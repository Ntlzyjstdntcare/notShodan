#!/usr/bin/env python

from shodan import Shodan
from shodan import APIError
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import EditPost, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from subprocess import call, check_output
from time import gmtime, strftime
import os
import shodan.helpers as helpers

api = Shodan('kJriccNQZOxl1LOigLKLxnb731GN5652')

ipAddress = ''
country = ''
city = ''
hostnames = ''
isp = ''
timestamp = ''
imageName = ''

client = Client('http://www.backdoored.io/xmlrpc.php', 'Ntlzyjstdntcare', 'Filesharer1!')


def callShodan():
    print 'In callShodan function'
    images = []
    screenshotsFilename = "screenshots"

    call(["shodan", "download", "screenshots.json.gz", "port:554 has_screenshot:true"])
    print 'Downloaded zip file'

    call(["./dump-images.py", "screenshots.json.gz", "images/"])
    print 'Dumped zip file into images directory'

    bannersTSDict = preloadBannerTimestamps(screenshotsFilename)
    print 'Generated lookup dictionary for image ips --> timestamps'

    count = 0
    for result in os.listdir(imagesDir):
        count += 1
        image = result.replace(".jpg", "")
        imageTimestamp = getTimestampFromBannerTSDict(bannersTSDict, image)
        if imageTimestamp != '':
            images.append((image, imageTimestamp))
    print 'date is: {0}'.format(time.strftime("%d/%m/%Y"))
    print 'Returning our updated list of images'
    return images;


def populateMetadata(image):
    print 'In populateMetadata function'
    for result in helpers.iterate_files('screenshots.json.gz'):

        if result['ip_str'] == image:
            print 'Found matching result!!!!!*****#########'
            global ipAddress
            if result['ip_str'] is not None:
              ipAddress = result['ip_str'] + '<br/>'
            else:
              ipAddress = ''

            global country
            if result['location']['country_name'] is not None:
              country = result['location']['country_name']
            else:
              country = ''

            global city
            if result['location']['city'] is not None:
              city = ', ' + result['location']['city']
            else:
              city = ''

            global hostnames
            if result['hostnames'] is not None:
              hostnames = str(result['hostnames']).replace("[", "").replace("]", "").replace("u", "") + '<br/>'
            else:
              hostnames = ''

            global isp
            if result['isp'] is not None:
              isp = result['isp'] + '<br/>'
            else:
              isp = ''

            global timestamp
            if result['timestamp'] is not None:
              timestamp = result['timestamp'].replace("T", " ") + '<br/>'
            else:
              timestamp = ''

           

def preloadBannerTimestamps(input_file):
    bannerTSDict = {}
    if not input_file.endswith('.json.gz'):
        input_file += '.json.gz'
    for result in helpers.iterate_files(input_file):
        bannerTSDict[result['ip_str']] = result['timestamp']
    return bannerTSDict


def getTimestampFromBannerTSDict(bannerTSDict, image):
    timestamp = ''
    if image in bannerTSDict:
        timestamp = bannerTSDict[image]
    return timestamp


def createPost(image):
    localFilename = 'images/{0}'.format(image + '.jpg')
    print 'image is: {0}'.format(localFilename)

    imageTimestamp = getTimestamp(image)

    wpFilename = image + imageTimestamp + '.jpg'

    data = {
            'name': '{0}'.format(wpFilename),
            'type': 'image/jpeg',
    }

    with open(localFilename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))

    print 'response is: {0}'.format(response)

    month = strftime("%m", gmtime())

    post = WordPressPost()
    post.title = country + city
    post.content = '[caption id="" align="alignnone" width ="640"]<img src="http://www.backdoored.io/wp-content/uploads/2016/' + month + '/' + wpFilename.replace(":", "") + '">' + ipAddress + hostnames + isp + timestamp + country + city + '[/caption]'
    post.id = client.call(NewPost(post))
    post.post_status = 'publish'
    client.call(EditPost(post.id, post))


newList = callShodan()
print 'Created copy of list'
print 'About to wait for 10 seconds...'
time.sleep(10)

while True:
    print 'In infinite loop'

    month = strftime("%m", gmtime())
    print 'month is: {0}'.format(month)

    global newList
    for image in callShodan(): 
        if image[1] != '':    
            if image not in newList:
                print 'Image not in copied list: {0}, {1}'.format(image[0], image[1])
                populateMetadata(image[0])
                createPost(image[0])
                newList.append(image)
    print 'Waiting for 2 hours in loop...'
    time.sleep(7200)
