#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import MySQLdb
import facebook
from datetime import datetime
from time import strptime
import dateutil.parser as dateparser

# Facebook app token
app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'

def fetch_updated_event_times_data(event_id):
    
    event = None
    
    try:
        graph = facebook.GraphAPI(access_token=app_token, version='2.2')

        event = graph.get_objects(ids=[event_id],
                                  fields='id, start_time, end_time, updated_time ',
                                  date_format='U')
    except facebook.GraphAPIError:
        print ('Facebook-graph error fetching updated event data. Event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)

    if (event is None) or (len(event) == 0):
        return None, None, None

    event_data = event[event_id]
    event_start_time = event_data.get('start_time', None)  # Time format is String here, convert to DB time format..
    event_end_time = event_data.get('end_time', None)

    # Remove timezone from facebook datetime
    if event_start_time is not None:
        event_start_time = dateparser.parse(event_start_time)
        event_start_time = str(event_start_time.replace(tzinfo=None))

    if event_end_time is not None:
        event_end_time = dateparser.parse(event_end_time)
        event_end_time = str(event_end_time.replace(tzinfo=None))

    return event_start_time, event_end_time


def execute_update_query(conn, event_id, event_start_time, event_end_time):

    times_update_query = 'UPDATE Event_Time ' \
                          'SET start_time=%s, ' \
                          'end_time=%s, ' \
                          'update_time=NOW()' \
                          'WHERE event_id=\'%s\''

    event_times_parameters = (str(event_start_time),
                              str(event_end_time),
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
        conn.rollback()  # Any
        tb = traceback.format_exc()
        print(tb)
        #  other exception should be rolled back to protect DB integrity


def update_event_times(conn, event_id):
    """ Fetches the updated event-times details using the facebook graph-api (start, end times),
        and updates the event_times entry at the Event-Times table in the database accordingly.
        @:return True if the update process succeeded, False is failed
    """
    try:
        event_start_time, event_end_time = fetch_updated_event_times_data(event_id)

        if (event_start_time is None) or \
           (event_end_time is None):
            return False

        execute_update_query(conn, event_id, event_start_time, event_end_time)

        return True
    except Exception:
        print ('Error updating event times for event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)
        return False


if __name__ == '__main__':

    con = MySQLdb.connect('localhost', 'DbMysql08', 'DbMysql08', 'DbMysql08', charset='utf8')
    update_event_times(con, '1782896528641706')