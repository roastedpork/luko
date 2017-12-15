#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
from speech_recognition.msg import Intent
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import sys
import json

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search



class SearchNode(object):
    def __init__(self):
        self.sub = rospy.Subscriber("search_images/query", Intent, self.callback, queue_size = 10)
        self.pub = rospy.Publisher("search_images/status_flag", Intent, queue_size = 10)

        if os.path.isfile("/home/pi/searchRes/loaded.txt"):
            with open("/home/pi/searchRes/loaded.txt","r") as file:
                self.loaded = json.load(file)
        else:
            self.loaded = []

        print "list of preloaded images: " + str(self.loaded)

    def callback(self,ros_data):
        params = json.loads(ros_data.params)
        print params
        if ros_data.action == 'image':
            query_text = " ".join(params['image'])
            rospy.loginfo("searching for images of '%s'..." % (query_text))
    
    
            # search parameters
            query = query_text + '' if params['no_blk'] == "1" else " black background"
            search = query.replace(" ","+")
            prefix = query.replace(" ","_")
            max_images = 5
            save_directory = '/home/pi/searchRes'
    
            if prefix not in self.loaded:
    
                # url header configs
                image_type="Action"
                url="https://www.google.co.in/search?q="+search+"&source=lnms&tbm=isch"
                header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
                soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
    
                # parsing for all links to high res images in html
                ActualImages=[]
                for a in soup.find_all("div",{"class":"rg_meta"}):
                    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
                    ActualImages.append((link,Type))
    
                # retrieving all high res images
                rospy.loginfo("Downloading images of '%s'..." % (query_text))
                count = 0
                if not os.path.exists(save_directory): os.mkdir(save_directory)
                for i , (img , Type) in enumerate(ActualImages[0:max_images]):
                    try:
                        req = urllib2.Request(img, headers=header)
                        raw_img = urllib2.urlopen(req).read()
                        if len(Type)==0:
                            f = open(str(os.path.join(save_directory , prefix + "_%02d.jpg"%(i))), 'wb')
                        else :
                            f = open(str(os.path.join(save_directory , prefix + "_%02d."%(i) + Type)), 'wb')
                        f.write(raw_img)
                        f.close()
                        rospy.loginfo( "Image %02d of %02d downloaded..." % (i+1,max_images))
                        count += 1
                    except Exception as e:
                        print("could not load : "+img)
                        print(e)
    
                resp = Bool()
                resp.data = True if count > 0 else False
                self.pub.publish(resp)
    
    
                if resp.data: 
                    self.loaded.append(prefix)
                    with open("/home/pi/searchRes/loaded.txt","w") as file:
                        json.dumps(self.loaded,file)
            else:
                rospy.loginfo("Images of '%s' has previously been downloaded" % (query_text))
                resp = Intent()
                resp.action = "image"
                resp.params = json.dumps({'prefix':prefix})
                self.pub.publish(resp)

if __name__ == '__main__':
    print "Initializing google images search node..."
    rospy.init_node('search_google_api',anonymous=True)
    r = rospy.Rate(10)
    search = SearchNode()
    rospy.loginfo("Image Search Node ready!")    

    rospy.spin()

    rospy.loginfo("Image Search Node exiting")
