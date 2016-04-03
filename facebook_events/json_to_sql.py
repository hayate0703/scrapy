#!flask/bin/python
# -*- coding: utf_8 -*-

from app import db, models
import json
import os
import datetime

def get_data_from_json(filename):
    with open(filename, 'r') as f:
        page_id = filename.split(".")[0]
        data = json.load(f)
        for event in data[str(page_id)]['events']['data']:
            if event.has_key('place'):
                event_info = models.Event(
                    event_id = event['id'],
                    name = event['name'],
                    description = event['description'],
                    time = datetime.datetime.strptime(event['start_time'].split("+")[0],"%Y-%m-%dT%H:%M:%S"),
                    picture_url = event['picture']['data']['url'],
                    cover_url = event['cover']['source'],
                    going = event['attending_count'],
                    interested = event['maybe_count'],
                    ticket_url = event['ticket_uri'],
                    city = event['place']['location']['city'],
                    place = event['place']['name'],
                    street = event['place']['location']['street'],
                    latitude = event['place']['location']['latitude'],
                    longitude = event['place']['location']['longitude']
                )
                db.session.add(event_info)
                db.session.commit()
            else:
                event_info = models.Event(
                    event_id = event['id'],
                    name = event['name'],
                    description = event['description'],
                    time = datetime.datetime.strptime(event['start_time'].split("+")[0],"%Y-%m-%dT%H:%M:%S"),
                    picture_url = event['picture']['data']['url'],
                    cover_url = event['cover']['source'],
                    going = event['attending_count'],
                    interested = event['maybe_count'],
                    ticket_url = event['ticket_uri'],
                )
                db.session.add(event_info)
                db.session.commit()


if __name__ == '__main__':
    filename = '242078635893289.json'
    get_data_from_json(filename)

