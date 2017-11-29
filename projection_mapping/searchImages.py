#!/usr/bin/env python3

from bs4 import BeautifulSoup as Soup
from html.parser import HTMLParser
import json
import urllib


#programtically go through google image ajax json return and save links to list#
#num_images is more of a suggestion                                            #  
#it will get the ceiling of the nearest 100 if available                       #
def get_links(query_string, num_images):
    #initialize place for links
    links = []
    #step by 100 because each return gives up to 100 links
    for i in range(0,num_images,100):
        url = 'https://www.google.com/search?q='+query_string#+'\
        #&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start='+str(i)+'\
        #&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg.i&ijn=1&asearch=ichunk&async=_id:rg_s,_pms:s'

        #set user agent to avoid 403 error
        request = urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0'}) 
        r = urllib.request.urlopen(request)

        #returns json formatted string of the html
        html = urllib.request.urlopen(request).read().decode('utf-8')

        #use BeautifulSoup to parse as html
        new_soup = Soup(html,'html5lib')

        #all img tags, only returns results of search
        imgs = new_soup.find_all('img')

        #loop through images and put src in links list
        for j in range(len(imgs)):
            links.append(imgs[j]["src"])

    return links


def search_images(term,num_images):
    img_links = get_links(term,num_images)

    for i,l in enumerate(img_links):
        urllib.request.urlretrieve(l, "images/"+term+"_%02d.jpg"%(i))

if __name__ == '__main__':
    term = "cat"
    search_images(term,10)
