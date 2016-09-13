#!/usr/bin/env python
#coding=utf-8

import click
import gc
import gzip
import os
import simplejson
import sys
import time
import json

import shodan
import shodan.helpers as helpers
import shutil

api = shodan.Shodan('kJriccNQZOxl1LOigLKLxnb731GN5652')

imagesDirname = 'C:\Users\Grand Gobshite\htdocs\images'
if not os.path.exists(imagesDirname):
    os.mkdir(imagesDirname)


def callShodan():
    print 'In callShodan function'
    images = []

    downloadLimit = 5
    screenshotsFilename = "screenshots"
    imagesDir = "images"
    searchQuery = "port:554 has_screenshot:true"

    download(downloadLimit, screenshotsFilename, searchQuery)
    print 'Downloaded zip file'

    doDumpImages(screenshotsFilename, imagesDir)
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
    print 'Length of list returned by callShodan is: ' + str(len(images))
    return images;


def download(limit, filename, query):
    """Download search results and save them in a compressed JSON file."""
    print '...attempting shodan query & result download...'
    print ''
    print '*** *** *** *** *** *** *** *** *** ***'
    print 'Query search terms: ' + query
    print 'Query results limited to: ' + str(limit)
    print 'Query results filename: ' + filename
    print '*** *** *** *** *** *** *** *** *** ***'

    # Make sure the user didn't supply an empty string
    if query == '':
        raise click.ClickException('Empty search query')

    filename = filename.strip()
    if filename == '':
        raise click.ClickException('Empty filename')

    # Add the appropriate extension if it's not there atm
    if not filename.endswith('.json.gz'):
        filename += '.json.gz'

    try:
        total = api.count(query)['total']
        info = api.info()
    except Exception,e:
        print str(e)
        raise click.ClickException('Error querying Shodan API...')


    # Print some summary information about the download request
    print ''
    print '*** *** *** *** *** *** *** *** *** ***'
    click.echo('Search query:\t\t\t%s' % query)
    click.echo('Total number of results:\t%s' % total)
    click.echo('Query credits left:\t\t%s' % info['unlocked_left'])
    click.echo('Output file:\t\t\t%s' % filename)
    print '*** *** *** *** *** *** *** *** *** ***'
    print ''

    if limit > total:
        limit = total

    # A limit of -1 means that we should download all the data
    if limit <= 0:
        limit = total

    with gzip.open(filename, 'w') as fout:
        count = 0
        try:
            cursor = api.search_cursor(query, minify=False)
            with click.progressbar(cursor, length=limit) as bar:
                for banner in bar:
                    writeBanner(fout, banner)
                    count += 1

                    if count >= limit:
                        break
        except:
            pass

        # Let the user know we're done
        if count < limit:
            pass   
            click.echo(click.style('Notice: fewer results were saved than requested', 'yellow'))
        click.echo(click.style('Saved %s results into file %s' % (count, filename), 'green'))


def writeBanner(fout, banner):
    line = simplejson.dumps(banner) + '\n'
    fout.write(line.encode('utf-8'))


def doDumpImages(input_file, output_dir):
 # Make sure the directory exists
 if not os.path.exists(output_dir):
    os.mkdir(output_dir)

 if not input_file.endswith('.json.gz'):
        input_file += '.json.gz'

 for banner in helpers.iterate_files(input_file):
    # Try to grab the screenshot from the banner
    screenshot = helpers.get_screenshot(banner)

    # If we found a screenshot then create a file w/ the data
    if screenshot:
        # Create the file handle
        image = open('{}/{}.jpg'.format(output_dir, banner['ip_str']), 'w')

        # Write the image data which is stored using base64 encoding
        image.write(screenshot['data'].decode('base64'))


def populateMetadata(image):
    print 'In populateMetadata function'
    for result in helpers.iterate_files('screenshots.json.gz'):

         if result['ip_str'] == image:
            global ipAddress
            
            try:
                if result['ip_str'] is not None:
                  ipAddress = str(result['ip_str'])
                else:
                  ipAddress = ''
            except Exception as error:
                print ""

            global asn
            try:
                if 'asn' in result:
                  asn = str(result['asn'])
                else:
                  asn = ''
            except Exception as error:
                print ""     

            global hashCode
            try:
                if result['hash'] is not None:
                  hashCode = str(result['hash'])
                else:
                  hashCode = ''
            except Exception as error:
                print ""

            global ip
            try:
                if result['ip'] is not None:
                  ip = str(result['ip'])
                else:
                  ip = ''
            except Exception as error:
                print ""  

            global transport
            try:
                if result['transport'] is not None:
                  transport = str(result['transport'])
                else:
                  transport = ''
            except Exception as error:
                print ""  

            global port
            try:
                if result['port'] is not None:
                  port = str(result['port'])
                else:
                  port = ''
            except Exception as error:
                print ""  

            global region_code
            try:
                if result['location']['region_code'] is not None:
                  region_code = str(result['location']['region_code'])
                else:
                  region_code = ''
            except Exception as error:
                print ""  

            global area_code
            try:
                if result['location']['area_code'] is not None:
                  area_code = str(result['location']['area_code'])
                else:
                  area_code = ''
            except Exception as error:
                print ""  

            global longitude
            try:
                if result['location']['longitude'] is not None:
                  longitude = str(result['location']['longitude'])
                else:
                  longitude = ''
            except Exception as error:
                print ""  

            global country_code3
            try:
                if result['location']['country_code3'] is not None:
                  country_code3 = str(result['location']['country_code3'])
                else:
                  country_code3 = ''
            except Exception as error:
                print ""  

            global latitude
            try:
                if result['location']['latitude'] is not None:
                  latitude = str(result['location']['latitude'])
                else:
                  latitude = ''
            except Exception as error:
                print ""  

            global postal_code
            try:
                if result['location']['postal_code'] is not None:
                  postal_code = str(result['location']['postal_code'])
                else:
                  postal_code = ''
            except Exception as error:
                print ""  

            global dma_code
            try:
                if result['location']['dma_code'] is not None:
                  dma_code = str(result['location']['dma_code'])
                else:
                  dma_code = ''
            except Exception as error:
                print ""  

            global country_code
            try:
                if result['location']['country_code'] is not None:
                  country_code = str(result['location']['country_code'])
                else:
                  country_code = ''
            except Exception as error:
                print ""  

            global domains
            try:
                if result['domains'] is not None:
                  domains = str(result['domains'])
                else:
                  domains = ''
            except Exception as error:
                print ""  

            global org
            try:
                if result['org'] is not None:
                  org = str(result['org'])
                else:
                  org = ''
            except Exception as error:
                print ""  

            global OS
            try:
                if result['os'] is not None:
                  OS = str(result['os'])
                else:
                  OS = ''
            except Exception as error:
                print ""  

            global shodan
            try:
                if result['_shodan'] is not None:
                  shodan = str(result['_shodan'])
                else:
                  shodan = ''
            except Exception as error:
                print ""  

            global country
            try:
                if result['location']['country_name'] is not None:
                  country = str(result['location']['country_name'])
                else:
                  country = ''
            except Exception as error:
                print ""  

            global city
            try:
                if result['location']['city'] is not None:
                  city = str(result['location']['city'])
                else:
                  city = ''
            except Exception as error:
                print ""  

            global hostnames
            try:
                if result['hostnames'] is not None:
                  hostnames = str(result['hostnames']).replace("[", "").replace("]", "").replace("u", "")
                else:
                  hostnames = ''
            except Exception as error:
                print ""  

            global isp
            try:
                if result['isp'] is not None:
                  isp = str(result['isp'])
                else:
                  isp = ''
            except Exception as error:
                print ""  

            global timestamp
            try:
                if result['timestamp'] is not None:
                  timestamp = str(result['timestamp']).replace("T", " ")
                else:
                  timestamp = ''
            except Exception as error:
                print ""      


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


def populateAndWriteJson():
    print 'In populateJson function'
    data = {}
    data['ipAddress'] = ipAddress
    data['country'] = country
    data['city'] = city
    data['hostnames'] = hostnames 
    data['isp'] = isp
    data['timestamp'] = timestamp 
    data['asn'] = asn
    data['hashCode'] = hashCode
    data['ip'] = ip
    data['transport'] = transport
    data['port'] = port
    data['region_code'] = region_code
    data['area_code'] = area_code 
    data['longitude'] = longitude
    data['country_code3'] = country_code3
    data['latitude'] = latitude
    data['postal_code'] = postal_code
    data['dma_code'] = dma_code
    data['country_code'] = country_code
    data['domains'] = domains 
    data['org'] = org
    data['OS'] = OS 
    data['shodan'] = shodan

    with open('C:\Users\Grand Gobshite\htdocs\metadata.json', 'w') as outfile:
        json.dump(data, outfile)
    time.sleep(10)
    

newList = callShodan()
print 'Length of initial list is: ' + str(len(newList))
print 'Created copy of list'
print 'About to wait for 10 seconds...'
time.sleep(10)

while True:
    print 'In infinite loop'

    month = time.strftime("%m", time.gmtime())
    print 'month is: {0}'.format(month)

    for image in newList: 
        populateMetadata(image[0])
        populateAndWriteJson()
    
    print 'Waiting for 20 seconds in loop...'
    time.sleep(20)
