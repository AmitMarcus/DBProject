#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import MySQLdb
import facebook

# Facebook app token
app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'

def fetch_updated_event_times_data(event_id):

    try:
        graph = facebook.GraphAPI(access_token=app_token, version='2.2')

        event = graph.get_objects(ids=[event_id],
                                           fields='id, start_time, end_time, update time')
    except facebook.GraphAPIError:
        print ('Facebook-graph error fetching updated event data. Event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)

    if (event is None) or (len(event) == 0):
        return None, None, None, None, None

    event_data = event[event_id]
    event_start_time = event_data.get('start_time',
                                 None)  # Time format is String here, convert to DB time format..
    event_end_time = event_data.get('end_time', None)
    event_updated_time = event_data.get('updated_time', None)

    return event_start_time, event_end_time, event_updated_time


def execute_update_query(conn, event_id, event_start_time, event_end_time, event_updated_time):

    times_update_query = 'UPDATE Event_Time ' \
                          'SET start_time=\'%s\', ' \
                          'end_time=\'%s\', ' \
                          'updated_time=\'%s\' ' \
                          'WHERE event_id=\'%s\''

    event_times_parameters = (str(event_start_time),
                              str(event_end_time),
                              str(event_updated_time),
                              long(event_id))

    try:
        # Create cursor for executing UPDATE query..
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        cur.execute(times_update_query, event_times_parameters)
    except MySQLdb.IntegrityError:
        print("Skipping duplicate Event-Time entry: " + str(event_id))
    except MySQLdb.OperationalError:
        pass  # Silently ignore constraint errors, this is the database protecting against bad FB records..
    except Exception:
        con.rollback()  # Any other exception should be rolled back to protect DB integrity

def update_event_times(conn, event_id):
    """ Fetches the updated event-times details using the facebook graph-api (start, end, updated times),
        and updates the event_times entry at the Event-Times table in the database accordingly.
        @:return True if the update process succeeded, False is failed
    """
    try:
        event_start_time, event_end_time, event_updated_time = fetch_updated_event_times_data(event_id)

        if (event_start_time is None) or \
           (event_end_time is None) or \
           (event_updated_time is None):
            return False

        execute_update_query(conn, event_id, event_start_time, event_end_time, event_updated_time)

        return True
    except Exception:
        print ('Error updating event times for event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)
        return False