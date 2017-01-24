#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import MySQLdb
import facebook

# Facebook app token
app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'


def fetch_updated_event_guests_data(event_id):
    """ Grabs up to date fields from facebook """

    try:
        event = None
        graph = facebook.GraphAPI(access_token=app_token, version='2.2')

        # We don't fetch attending count since it's indexed and slow to update (this is a design decision),
        # and don't fetch declined / maybe since they are meaningless for facebook  public events (always 0).
        # The shipped version of our app uses only an app key and not a user key (which is required to access
        # private events that make use of these fields)
        event = graph.get_objects(ids=[event_id],
                                           fields='id,noreply_count,interested_count')

    except facebook.GraphAPIError:
        print ('Facebook-graph error fetching updated event data. Event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)

    if (event is None) or (len(event) == 0):
        return None, None

    event_data = event[event_id]

    event_interested_count = event_data.get('interested_count', None)
    event_noreply_count = event_data.get('noreply_count', None)

    return event_interested_count, event_noreply_count


def execute_update_query(conn, event_id, event_interested_count, event_noreply_count):

    guests_update_query = 'UPDATE Event_Guests ' \
                          'SET interested_count=\'%s\', ' \
                          'noreply_count=\'%s\' ' \
                          'WHERE event_id=\'%s\''

    event_guests_parameters = (event_interested_count,
                               event_noreply_count,
                               long(event_id))

    try:
        # Create cursor for executing UPDATE query..
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        cur.execute(guests_update_query, event_guests_parameters)
        # - Autocommit occurs here -

    except MySQLdb.IntegrityError:
        print("Skipping duplicate Event-Guest entry: " + str(event_id))
    except MySQLdb.OperationalError:
        pass  # Silently ignore constraint errors, this is the database protecting against bad FB records..
    except Exception:
        # Any other exception should be rolled back to protect DB integrity
        # autocommit mode takes care of rollback for us in case of an error, all that remains is to handle
        # the error..
        tb = traceback.format_exc()
        print(tb)

def update_event_guests(conn, event_id):
    """ Fetches the updated event-guests interested / no-reply count using the facebook graph-api..
        and updates the event_guests entry at the Event-Guests table in the database accordingly.
        @:return True if the update process succeeded, False is failed
    """
    try:
        event_interested_count, event_noreply_count = fetch_updated_event_guests_data(event_id)

        if (event_interested_count is None) or \
           (event_noreply_count is None):
            return False

        execute_update_query(conn, event_id, event_interested_count, event_noreply_count)

        return True
    except Exception:
        print ('Error updating event guests for event_id: ' + str(event_id))
        tb = traceback.format_exc()
        print(tb)
        return False