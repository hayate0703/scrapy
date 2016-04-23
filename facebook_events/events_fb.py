#!/usr/bin/python

import time
import json
import logging
import os
import requests
from coorcal import generate_coordinate

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG, format='%(levelname)s:%(message)s')

# Load config from file config.json
with open('config.json', 'r') as f:
    args = json.load(f)

# Get App Access Token
token = requests.get("https://graph.facebook.com/v2.5/oauth/access_token?client_id={0}&client_secret={1}&&grant_type=client_credentials".format(
    args["client_id"], args["client_secret"]))

# Create folder results to export results to
if not os.path.exists("./results"):
    os.makedirs("./results")


def get_page_ids(lat, lon):
    '''
    Get pages's ID from a location. Return a list of all ID.
    '''
    pages_id = requests.get("https://graph.facebook.com/v2.5/search?type=place&q={0}&center={1},{2}&distance={3}&limit={4}&fields=id&access_token={5}".format(
        args["keyword"],
        lat, lon,
        args["distance"],
        args["limit"],
        token.content.split('"')[3]))
    # Create a list of all ID
    pages_id_list = [i.values()[0] for i in pages_id.json()['data']]
    return pages_id_list


def events_from_page_id(id):
    '''
    For each page ID, find all event (if have) of that Page from today.
    Return a dictionary of page's infos and it's events.
    '''
    events = requests.get("https://graph.facebook.com/v2.5/?ids={0}&fields=events.fields(id,name,start_time,description,place,type,category,ticket_uri,cover.fields(id,source),picture.type(large),attending_count,declined_count,maybe_count,noreply_count).since({1}),id,name,cover.fields(id,source),picture.type(large),location&access_token={2}".format(
        id, time.strftime("%Y-%m-%d"), token.content.split('"')[3]))
    return events.json()

if __name__ == '__main__':
    CIRCLE = (21.027875, 105.853654, 10000,)
    for point in generate_coordinate(*CIRCLE, scan_radius=args["distance"]):
        for page_id in get_page_ids(point[0], point[1]):
            if 'events' in events_from_page_id(page_id).values()[0]:
                file_name = "./results/" + page_id + ".json"
                with open(file_name, 'wb') as f:
                    json.dump(events_from_page_id(page_id), f, indent=4)
            else:
                pass
