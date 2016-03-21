#!/usr/bin/python

import argparse
import csv
import json
import requests
import time

parser = argparse.ArgumentParser(
    description='Export crawl result to file through ScrapingHub API')
parser.add_argument('-l', '--link', type=str, help='Job\'s URL')
parser.add_argument(
    '-f', '--format', type=str, help='File format', default='csv')
args = parser.parse_args()

url_of_job = args.link.split('/')

# Config
api = 'e344e086149a418ebaffa556ff7190bd'

# If URL is https://dash.scrapinghub.com/p/48357/job/1/2/ , project ID is
# 48357, spider ID is 1, job ID is 2
project = url_of_job[4]
spider = url_of_job[6]
job = url_of_job[7]

# Format_type should be on of : json, jl, csv, text, xml
format_type = args.format

# Fields is required if format is CSV. No space after comma.
fields = 'url,title,author,date,content'

if format_type != 'csv':
    url = "https://storage.scrapinghub.com/items/{0}/{1}/{2}/?format={3}&apikey=".format(
        project, spider, job, format_type) + api
else:
    url = "https://storage.scrapinghub.com/items/{0}/{1}/{2}/?format={3}&fields={4}&include_headers=1&apikey=".format(
        project, spider, job, format_type, fields) + api

# Send request to API Url
r = requests.get(url)

# Named file with Project, Spider and Job ID, with specific date, time
file_name = str(project + "_" + spider + "_" + job + "_" +
                time.strftime("%Y%m%d-%H%M%S")) + '.' + format_type


if format_type == 'json':
    with open(file_name, 'wb') as f:
        json.dump(r.json(), f)
else:
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

print "Data were extract to :", file_name
print "URL: ", r.url
