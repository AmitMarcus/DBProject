#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import sys
import time
import traceback

import MySQLdb
import facebook
from requests.exceptions import ConnectionError

from fb_config import user_token
from fb_config import app_token
from fb_config import database_hostname
import fb_populate as fb_db


def populate_db():
    """ Populates database from Json files downloaded """

    # Connect to Database - we test the connection as early as possible.
    # If there are connection problems we want to quit as early as possible in the process..
    con = MySQLdb.connect(database_hostname, 'DbMysql08', 'DbMysql08', 'DbMysql08', charset='utf8')
    con.close()
    con = None

    # We support insertion of multiple download processes at once.
    # Just specify their paths here.
    # (We expect under each path to find: "data.json", and a folder called "COMMENTS" with comment json files..
    fb_db.parse_dumped_jsons('Take1/')
    fb_db.parse_dumped_jsons('Take2/')
    fb_db.parse_dumped_jsons('Take3/')
    fb_db.parse_dumped_jsons('Take4/')
    fb_db.commit_dictionaries_to_db()


def extract_data():
    """
    Extracts some Events & Comments from Facebook, by keyword search queries..
    Data fetched using Facebook Python API: http://facebook-sdk.readthedocs.io/en/latest/install.html
    keyword.text is expected to exist in the same folder as this script (each line is a keyword to be searched)..
    """

    graph = facebook.GraphAPI(access_token=app_token, version='2.2')

    print('Connected successfully to Facebook-GraphAPI..')
    print('Initiating event search queries by keywords:')

    event_ids = []
    with open('keywords.txt') as keywords_file:
        for key in keywords_file:
            print(key)
            search_results = graph.request('search',
                                           {'access_token': user_token,
                                            'q': key,
                                            'type': 'event'})['data']
            for entry in search_results:
                event_id = entry['id']
                if event_id not in event_ids:
                    event_ids.append(event_id)

    events = None

    print('Fetching comments from feed of each event..:')

    # A maximum of 50 ids is allowed per query, divide to multiple queries
    while len(event_ids) > 0:
        event_ids_batch = event_ids[:49]
        new_events = graph.get_objects(ids=event_ids_batch,
                                       fields='id,name,category,description,cover,' +
                                              'start_time,end_time,timezone,place,' +
                                              'attending_count,declined_count,maybe_count,' +
                                              'noreply_count,interested_count,' +
                                              'can_guests_invite,guest_list_enabled,is_canceled,' +
                                              'ticket_uri,updated_time,' +
                                              'owner,type')

        if events is None:
            events = copy.deepcopy(new_events)
        else:
            events.update(new_events)

        for event_id in event_ids_batch:
            try:
                # Ignore paging, fetch only a single page of comments
                comments = graph.get_connections(id=event_id, connection_name='feed')
                with open(event_id + '_comments.json', 'w') as comments_file:
                    json.dump(comments, comments_file, sort_keys=True, indent=4)
            except facebook.GraphAPIError:
                continue
            except ConnectionError:
                # Could happen when we exceed the max retries count..
                # Rest for one minute, then continue trying..
                print('Max retries exceeded with url.. Resting for 1 minute before retrying..')
                time.sleep(60)
                print('Retrying to fetch comments..')
                try:
                    # Ignore paging, fetch only a single page of comments
                    comments = graph.get_connections(id=event_id, connection_name='feed')
                    with open(event_id + '_comments.json', 'w') as comments_file:
                        json.dump(comments, comments_file, sort_keys=True, indent=4)
                except facebook.GraphAPIError:
                    print ('Facebook-graph error on feed for event: ' + str(event_id))
                    tb = traceback.format_exc()
                    print(tb)
                    continue
                except Exception:
                    print('General error on feed for event ' + str(event_id) + '.. Could not retry :(')
                    print('Proceeding to dump data.json, some comments may be missing')
                    tb = traceback.format_exc()
                    print(tb)
            except Exception:
                print('General error on feed for event ' + str(event_id))
                print('Proceeding to dump data.json, some comments may be missing')


        event_ids = event_ids[50:]

    # Each given id maps to an object the contains the requested fields.
    with open('data.json', 'w') as events_file:
        json.dump(events, events_file, sort_keys=True, indent=4)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Incorrect Usage. Try:')
        print('python db_extract download_data // Harvests selected events from facebook to local Json files')
        print('python db_extract populate_db   // Populates DB with data stored in Json files')
        exit(1)

    cmd = sys.argv[1]

    if cmd == 'download_data':
        extract_data()
    elif cmd == 'populate_db':
        populate_db()
    else:
        print('Incorrect Usage. Try:')
        print('python db_extract download_data // Harvests selected events from facebook to local Json files')
        print('python db_extract populate_db   // Populates DB with data stored in Json files')
        exit(1)
