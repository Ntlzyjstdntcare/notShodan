#!/usr/bin/env python

from shodan import Shodan
from shodan import APIError
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
# from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import EditPost, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from subprocess import call, check_output
from datetime import datetime
import os
import shodan.helpers as helpers
# import arrow
api = Shodan('kJriccNQZOxl1LOigLKLxnb731GN5652')
# MAX_SCREENS = 24

ipAddress = ''
country = ''
city = ''
hostnames = ''
isp = ''
timestamp = ''
imageName = ''

client = Client('http://www.backdoored.io/xmlrpc.php', 'Ntlzyjstdntcare', 'Filesharer1!')

# try:
# # Search Shodan
#   results = api.search('port:554 has_screenshot:true')
# # Show the results
#   print 'Results found: %s' % results['total']
#   for result in results['matches']:
#     print 'IP: %s' % result['ip_str']
#     print result['data']
#     print ''
# except APIError, e:
#   print 'Error: %s' % e
# sys.print

# Search Shodan
# results = api.search('port:554 has_screenshot:true')
# images = []

# callShodan()


def callShodan():
    print 'In callShodan function'
    images = []
    
# print 'Number of results: %s' % len(results['matches'])

    call(["shodan", "download", "screenshots.json.gz", "port:554 has_screenshot:true"])
    print 'Downloaded zip file'

    call(["./dump-images.py", "screenshots.json.gz", "images/"])
    print 'Dumped zip file into images directory'
# for result in results['matches']:

    for result in os.listdir('images/'):	
        #print '{0}'.format(result)

        images.append(result.replace(".jpg", ""))
        #print 'Number of images: {0}'.format(len(images))

    # imageName = images[0].replace(".jpg", "")
    # print 'image name is: {0}'.format(imageName)
    print 'Returning our updated list of images'
    return images;


def populateMetadata(image):
    print 'In populateMetadata function'
    for result in helpers.iterate_files('screenshots.json.gz'):
	# print 'x'

        if result['ip_str'] == image:
            print 'Found matching result!!!!!*****#########'
            #print 'Result is : {0}'.format(result)
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
              hostnames = result['hostnames'].replace("[", "").replace("]", "").replace("u", "") + '<br/>'
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



def createPost(image):
    filename = 'images/{0}'.format(image + '.jpg')
    print 'image is: {0}'.format(filename)

    data = {
	    'name': '{0}'.format(image + '.jpg'),
	    'type': 'image/jpeg',
    }

    with open(filename, 'rb') as img:
	    data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))

    print 'response is: {0}'.format(response)

    if datetime.month.len == 1:
      month = '0' + datetime.month
    else:
      month = datetime.month	

    post = WordPressPost()
    post.title = country + city
    post.content = '<img style="float:left" src="http://www.backdoored.io/wp-content/uploads/2016/' + month + '/' + image + '.jpg' + '">' + ipAddress + hostnames + isp + timestamp + country + city
    post.id = client.call(NewPost(post))
    post.post_status = 'publish'
    client.call(EditPost(post.id, post))




newList = callShodan()
print 'Created copy of list'
print 'About to wait for 10 seconds...'
time.sleep(10)

while True:
    ##if result of this is different to newList call other function that makes post, and add them to newList
    print 'In infinite loop'
    global newList
    for image in callShodan():
        if image not in newList:
            print 'Image not in copied list: {0}'.format(image)
            populateMetadata(image)
            createPost(image)
            newList.append(image)
    print 'Waiting for 10 seconds in loop...'           
    time.sleep(10)        



	# host = api.host(result['ip_str'], history=True)

	# for banner in host['data']:
		# print '\nThis is a banner: {0}'.format(banner)





#     #print 'x'
  ##  host = result['ip_str']
    ##host = api.host(host)
    

#    for banner in result['data']:
    ##print 'Number of banners: %s' % len(host['data'])
    ##for banner in host['data']:
        # print 'x'
    	# print """
     #            Port: %s
     #            Banner: %s

     #    """ % (banner['port'], banner['data'])
#     	print 'Banner opts: %s' % banner['screenshot']
    	#print banner
    ##	sort_key = time.time()
        # Extract the image from the banner data
      ##  if 'opts' in banner and 'screenshot' in banner['opts']:
        	# print 'This is the timestamp on the image: %s' % banner['timestamp']
            # Sort the images by the time they were collected so the GIF will loop
            # based on the local time regardless of which day the banner was taken.
            # timestamp = arrow.get(banner['timestamp']).time()
        	# print 'x'
        	
        ##    sort_key = banner['timestamp']
            # print '%s' % sort_key
            # print 'x'
          ##  screenshots.append((
            ##    sort_key,
              ##  banner['opts']['screenshot']['data']
            ##))
            ##print 'Number of screenshots: %s' % len(screenshots)
            # print 'banner is: {}'.format(banner)
            #print 'this is what is in opts: {0}'.format(banner['opts'])
            #print 'This is the screenshot: %s' % banner['opts']['screenshot']
            # Ignore any further screenshots if we already have MAX_SCREENS number of images
            # if len(screenshots) >= MAX_SCREENS:
            	# print 'Number of screenshots: %s' % len(screenshots)
                # break

# for banner in api.stream.banners():
#     if 'opts' in banner and 'screenshot' in banner['opts']:      
#         print 'x' 
#for screenshot in screenshots:
##print 'screenshot is: {0}'.format(screenshots[2][1])
# b64 = screenshots[2][1].decode('base64')
# print 'base64 screenshot is {0}'.format(b64)





#x = check_output(["ls", "-a", "-l"])
##print 'x is: {0}'.format(x)
# print 'This is the list of screenshots: %s' % screenshots['timestamp']      