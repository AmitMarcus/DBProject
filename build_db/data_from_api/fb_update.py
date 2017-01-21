#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import MySQLdb
import facebook

from fb_config import app_token
from fb_config import database_hostname


def fetch_updated_event_guests_data(event_id):

    try:
        graph = facebook.GraphAPI(access_token=app_token, version='2.2')

        event = graph.get_objects(ids=[event_id],
                                           fields='id, attending_count,declined_count,maybe_count,' +
                                                  'noreply_count,interested_count')
    except facebook.GraphAPIError:
        print ('Facebook-graph error fetching updated event data. Event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)

    if (event is None) or (len(event) == 0):
        return None, None, None, None, None

    event_data = event[event_id]
    event_attending_count = event_data.get('attending_count', None)
    event_declined_count = event_data.get('declined_count', None)
    event_interested_count = event_data.get('interested_count', None)
    event_maybe_count = event_data.get('maybe_count', None)
    event_noreply_count = event_data.get('noreply_count', None)

    return event_attending_count, event_declined_count, event_interested_count, event_maybe_count, event_noreply_count


def execute_update_query(event_id, event_attending_count, event_declined_count, event_interested_count,\
                         event_maybe_count, event_noreply_count):

    guests_update_query = 'UPDATE Event_Guests ' \
                          'SET attending_count=\'%s\', ' \
                          'declined_count=\'%s\', ' \
                          'maybe_count=\'%s\', ' \
                          'interested_count=\'%s\', ' \
                          'noreply_count=\'%s\' ' \
                          'WHERE event_id=\'%s\''

    event_guests_parameters = (event_attending_count,
                               event_declined_count,
                               event_maybe_count,
                               event_interested_count,
                               event_noreply_count,
                               long(event_id))

    try:
        con = MySQLdb.connect(database_hostname, 'DbMysql08', 'DbMysql08', 'DbMysql08', charset='utf8')

        # Create cursor for executing UPDATE query..
        cur = con.cursor(MySQLdb.cursors.DictCursor)

        cur.execute(guests_update_query, event_guests_parameters)
        con.commit()
    except MySQLdb.IntegrityError:
        print("Skipping duplicate Event-Guest entry: " + str(event_id))
    except MySQLdb.OperationalError:
        pass  # Silently ignore constraint errors, this is the database protecting against bad FB records..


def update_event_guests(event_id):
    """ Fetches the updated event-guests details using the facebook graph-api (number of attending, declined, etc),
        and updates the event_guests entry at the Event-Guests table in the database accordingly.
        @:return True if the update process succeeded, False is failed
    """

    try:
        event_attending_count, event_declined_count, event_interested_count,\
        event_maybe_count, event_noreply_count = fetch_updated_event_guests_data(event_id)

        if (event_attending_count is None) or \
           (event_declined_count is None) or \
           (event_interested_count is None) or \
           (event_maybe_count is None) or \
           (event_noreply_count is None):
            return False

        execute_update_query(event_id, event_attending_count, event_declined_count, event_interested_count,\
                             event_maybe_count, event_noreply_count)

        return True
    except Exception:
        print ('Error updating event guests for event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)
        return False