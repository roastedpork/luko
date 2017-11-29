#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool

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
        self.sub = rospy.Subscriber("search_images/query", String, self.callback, queue_size = 1)
        self.pub = rospy.Publisher("search_images/status_flag", Bool, queue_size = 1)

    def callback(self,ros_data):
	rospy.loginfo("searching for images of '%s'..." % (ros_data.data))
	print "searching for images of '%s'..." % (ros_data.data)

        # search parameters
        query = ros_data.data.replace(" ","+")
        max_images = 10
        save_directory = 'searchRes'

        # url header configs
        image_type="Action"
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

        # parsing for all links to high res images in html
        ActualImages=[]
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))

        # retrieving all high res images
        print "Downloading images of '%s'..." % (ros_data.data)
        prefix = ros_data.data.replace(" ","_")
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
            except Exception as e:
                print("could not load : "+img)
                print(e)

        resp = Bool()
        resp.data = True
        self.pub.publish(resp)
        rospy.loginfo( "Downloaded images of '%s'..." % (ros_data.data))

if __name__ == '__main__':
    print "Initializing google images search node..."
    rospy.init_node('search_google_api',anonymous=True)
    r = rospy.Rate(10)
    search = SearchNode()
    rospy.loginfo("Image Search Node ready!")    

    rospy.spin()

    rospy.loginfo("Image Search Node exiting")
