#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import traceback

import MySQLdb

from fb_config import database_hostname
from fb_config import categories

"""
    A module for:
    1) Inserting big amounts of data from Json files into the DB
    2) Populating the database with small insert / update requests and maintain integrity
"""

# These dictionaries accumulate meta data that multiple events may share, so we cache it until we're
# done iterating our fetched events and comments.
# Why we keep data in dictionaries: we want to avoid duplicate entries in the database.
# Although the columns are defined as "UNIQUE" in sql, inserting duplicate primary keys will
# trigger an integrity error, which we may catch and ignore.
# Another alternative is do execute a COUNT query every time we want to insert a new city / country / etc
# and check if it already exists in the database.
# Both methods may prolong the population process since we execute additional queries to the db.
# Instead we chose a simple solution of caching and inserting all at once.
# Our chosen method requires modifications if it scales to huge amounts of data
# (program may run out of heap memory, etc).
places = {}
streets = {}
cities = {}
countries = {}
timezones = {}
owners = {}

# Also cache events and comments due to foreign key constraints. Must build above entities first.
comments = {}
events = {}

# Finally we keep track of ids couples for the association tables
event_owner_assoc = {}
event_place_assoc = {}


def category_enum_to_id(category_enum):

    if category_enum is None:
        return 999  # Empty facebook ids are represented by special other id

    category_id, category_name = categories[category_enum.encode('UTF-8')]

    if category_id is None:
        return 999  # Avoid unknown categories by identifying them as other as well

    return category_id


def populate_categories(cur, con):
    """ Populates the database with the category names and ids """

    print('Populating categories..')
    category_fields = 'id,  name'
    insert_query = 'INSERT INTO Category (' + category_fields + ') VALUES (%s, %s)'

    for category_name, (category_id, category_title) in categories.iteritems():
        parameters = (long(category_id),
                      category_title.encode('UTF-8'))
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Category entry: " + str(category_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_timezones(cur, con):
    """ Populates the database with street entities """

    print('Populating timezones..')
    for timezone_name, timezone_id in timezones.iteritems():
        timezone_fields = 'id,  timezone'
        insert_query = 'INSERT INTO Timezone (' + timezone_fields + ') VALUES (%s, %s)'

        parameters = (long(timezone_id),
                      timezone_name.encode('UTF-8') if timezone_name is not None else None)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Timezone entry: " + str(timezone_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_streets(cur, con):
    """ Populates the database with street entities """

    print('Populating streets..')
    for street_key, (street_id, location_street, city_id) in streets.iteritems():
        street_fields = 'id,  name, city_id'
        insert_query = 'INSERT INTO Street (' + street_fields + ') VALUES (%s, %s, %s)'

        parameters = (long(street_id),
                      location_street.encode('UTF-8') if location_street is not None else None,
                      city_id)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Street entry: " + str(street_id))
        except MySQLdb.OperationalError:
            continue  # Silently ignore constraint errors, this is the database protecting against bad FB records..
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_places(cur, con):
    """ Populates the database with place entities """

    print('Populating places..')
    for place_id, (place_name, street_id, location_latitude, location_longitude) in places.iteritems():

        place_fields = 'id,  name, street_id, latitude, longitude'
        insert_query = 'INSERT INTO Place (' + place_fields + ') VALUES (%s, %s, %s, %s, %s)'

        parameters = (long(place_id),
                      place_name.encode('UTF-8') if place_name is not None else None,
                      long(street_id),
                      location_latitude,
                      location_longitude)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Place entry: " + str(place_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_cities(cur, con):
    """ Populates the database with city entities """

    print('Populating cities..')
    for location_city, (city_id, country_id) in cities.iteritems():
        city_fields = 'id,  name, country_id'
        insert_query = 'INSERT INTO City (' + city_fields + ') VALUES (%s, %s, %s)'

        parameters = (long(city_id),
                      location_city.encode('UTF-8') if location_city is not None else None,
                      long(country_id))
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate City entry: " + str(city_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_countries(cur, con):
    """ Populates the database with country entities """

    print('Populating countries..')
    for location_country, country_id in countries.iteritems():
        country_fields = 'id,  name'
        insert_query = 'INSERT INTO Country (' + country_fields + ') VALUES (%s, %s)'

        parameters = (long(country_id),
                      location_country.encode('UTF-8') if location_country is not None else None)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Country entry: " + str(country_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

    con.commit()
    print('Batch committed..')


def populate_owners(cur, con):
    """ Populates the database with owner entities """

    batch_size = 0

    print('Populating owners..')
    for owner_id, owner_name in owners.iteritems():
        owner_fields = 'id,  name'
        insert_query = 'INSERT INTO Owner (' + owner_fields + ') VALUES (%s, %s)'

        parameters = (long(owner_id),
                      owner_name.encode('UTF-8') if owner_name is not None else None)
        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Owner entry: " + str(owner_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0

    if batch_size > 0:
        con.commit()
    print('Batch committed..')


def populate_events(cur, con):
    """ Populates the database with the category names and ids """

    batch_size = 0

    print('Populating events..')
    for event_id, (event_name, event_attending_count, event_declined_count, event_maybe_count,event_interested_count, \
            event_noreply_count, event_is_canceled, event_description, event_category, \
            event_can_guests_invite, cover_url, event_ticket_uri, event_guest_list_enabled, \
            event_start_time, event_end_time, event_updated_time, timezone_id, event_type) \
            in events.iteritems():

        event_fields = 'id, name, is_canceled, category_id, ' \
                       'can_guest_invite, cover_source, event_ticket_uri, guest_list_enabled, event_type'

        event_guests_fields = 'event_id, attending_count, declined_count, maybe_count, interested_count, noreply_count'

        event_time_fields = 'event_id, timezone_id, start_time, end_time, update_time'

        event_desc_fields = 'event_id, description'

        # MSQLdb doesn't treat this string as a normal Python SQL string, so all fields are considered %s
        # (this is not a mistake..)
        events_insert_query = 'INSERT INTO Event (' + event_fields + ') ' \
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

        guests_insert_query = 'INSERT INTO Event_Guests (' + event_guests_fields + ') ' \
                                'VALUES (%s, %s, %s, %s, %s, %s)'

        time_insert_query = 'INSERT INTO Event_Time (' + event_time_fields + ') ' \
                                'VALUES (%s, %s, %s, %s, %s)'

        desc_insert_query = 'INSERT INTO Event_Desc_Search (' + event_desc_fields + ') ' \
                                'VALUES (%s, %s)'

        event_parameters = (long(event_id),
                            event_name.encode('UTF-8') if event_name is not None else None,
                            event_is_canceled,
                            category_enum_to_id(event_category),
                            event_can_guests_invite,
                            cover_url.encode('UTF-8') if cover_url is not None else None,
                            event_ticket_uri,
                            event_guest_list_enabled,
                            event_type.encode('UTF-8') if event_type is not None else None)

        event_guests_parameters = (long(event_id),
                            event_attending_count,
                            event_declined_count,
                            event_maybe_count,
                            event_interested_count,
                            event_noreply_count)

        event_time_parameters = (long(event_id),
                                 long(timezone_id),
                                 str(event_start_time),
                                 str(event_end_time),
                                 str(event_updated_time))

        desc_insert_parameters = (long(event_id),
                                  event_description.encode('UTF-8') if event_description is not None else None)

        try:
            cur.execute(events_insert_query, event_parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event entry: " + str(event_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        try:
            cur.execute(guests_insert_query, event_guests_parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event-Guest entry: " + str(event_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        try:
            cur.execute(time_insert_query, event_time_parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event-Time entry: " + str(event_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        try:
            cur.execute(desc_insert_query, desc_insert_parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event-Desc-Search entry: " + str(event_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 500:
            con.commit()
            batch_size = 0
            print('Batch committed..')

    if batch_size > 0:
        con.commit()
        print('Batch committed..')


def populate_event_owner_association(cur, con):
    """ Populates the database with event-owner ids """

    batch_size = 0

    print('Populating event-owner..')
    for event_id, owner_id in event_owner_assoc.iteritems():
        association_fields = 'event_id, owner_id'
        insert_query = 'INSERT INTO Event_Owner (' + association_fields + ') VALUES (%s, %s)'

        parameters = (long(event_id),
                      long(owner_id))

        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event-Owner entry: " + str(event_id) + ' , ' + str(owner_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0
            print('Batch committed..')

    if batch_size > 0:
        con.commit()
        print('Batch committed..')


def populate_event_place_association(cur, con):
    """ Populates the database with event-place ids """

    batch_size = 0

    print('Populating event-place..')
    for event_id, place_id in event_place_assoc.iteritems():

        association_fields = 'event_id, place_id'
        insert_query = 'INSERT INTO Event_Place (' + association_fields + ') VALUES (%s, %s)'

        parameters = (long(event_id),
                      long(place_id))
        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event-Owner entry: " + str(event_id) + ' , ' + str(place_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0
            print('Batch committed..')

    if batch_size > 0:
        con.commit()
        print('Batch committed..')


def populate_comments(cur, con):
    """ Populates the database with comment entities """

    batch_size = 0

    print('Populating comments..')
    for comment_id, (comment_msg, comment_time, event_id) in comments.iteritems():
        comment_fields = 'id,  message, updated_time, event_id'
        insert_query = 'INSERT INTO Comment (' + comment_fields + ') VALUES (%s, %s, %s, %s)'

        parameters = (comment_id,
                      comment_msg.encode('UTF-8') if comment_msg is not None else None,
                      str(comment_time),
                      event_id)
        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Comment entry: " + str(comment_id))
        except MySQLdb.OperationalError:
            continue    # Silently ignore constraint errors, this is the database protecting against bad FB records..

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0
            print('Batch committed..')

    if batch_size > 0:
        con.commit()
        print('Batch committed..')


def parse_dumped_jsons(path):
    """ Parses the data.json + X_comment.json files in the given path and adds their data to the dictionaries """

    with open(path + 'data.json', 'r') as data_file:
        data = json.load(data_file)

        # See types of event fields here:
        # https://developers.facebook.com/docs/graph-api/reference/event/
        for event in data.values():

            # Event parameters
            event_id = event.get('id', None)
            event_name = event.get('name', None)
            event_category = event.get('category', None)  # Enum of categories, see API link above
            event_description = event.get('description', None)
            event_start_time = event.get('start_time',
                                         None)  # Time format is String here, convert to DB time format..
            event_end_time = event.get('end_time', None)
            event_timezone = event.get('timezone', None)
            event_updated_time = event.get('updated_time', None)
            event_attending_count = event.get('attending_count', None)
            event_declined_count = event.get('declined_count', None)
            event_interested_count = event.get('interested_count', None)
            event_maybe_count = event.get('maybe_count', None)
            event_noreply_count = event.get('noreply_count', None)
            event_can_guests_invite = event.get('can_guests_invite', None)
            event_guest_list_enabled = event.get('guest_list_enabled', None)
            event_is_canceled = event.get('is_canceled', None)
            event_ticket_uri = event.get('ticket_uri', None)  # Link to buy tickets, string format
            event_owner = event.get('owner', None)

            if 'owner' in event:
                event_owner_id = event_owner.get('id', None)
                event_owner_name = event_owner.get('name', None)

            event_type = event.get('type', None)

            # Events have cover photos
            if (event.get('cover', None) is not None):
                cover_id = event.get('cover', None).get('id', None)  # Event cover photo id
                cover_offset_x = event.get('cover', None).get('offset_x', None)
                cover_offset_y = event.get('cover', None).get('offset_y', None)

                # Event cover photo url, need to access and download image raw bytes
                cover_url = event.get('cover', None).get('source',
                                                         None)

            # Each event has a unique place it occurs in, multiple events can share places
            if 'place' in event:
                place_id = event['place'].get('id', None)
                place_name = event['place'].get('name', None)
                place_rating = event['place'].get('overall_rating', None)

                # Each place has a location, which describes it's geographical data
                if 'location' in event['place']:
                    location_name = event['place']['location'].get('name', None)
                    location_region = event['place']['location'].get('region', None)
                    location_region_id = event['place']['location'].get('region_id', None)
                    location_city = event['place']['location'].get('city', None)
                    location_city_id = event['place']['location'].get('city_id', None)
                    location_country = event['place']['location'].get('country', None)
                    location_country_code = event['place']['location'].get('country_code', None)
                    location_latitude = event['place']['location'].get('latitude', None)
                    location_longitude = event['place']['location'].get('longitude', None)
                    location_street = event['place']['location'].get('street', None)
                    location_zipcode = event['place']['location'].get('zip', None)
                else:  # Null out unused params, so they don't get confused with other entries!
                    location_name = None
                    location_region = None
                    location_region_id = None
                    location_city = None
                    location_city_id = None
                    location_country = None
                    location_country_code = None
                    location_latitude = None
                    location_longitude = None
                    location_street = None
                    location_zipcode = None

            else:  # Null out unused params, so they don't get confused with other entries!
                place_id = None
                place_name = None
                place_rating = None
                place_id = None
                location_name = None
                location_region = None
                location_region_id = None
                location_city = None
                location_city_id = None
                location_country = None
                location_country_code = None
                location_latitude = None
                location_longitude = None
                location_street = None
                location_zipcode = None

            comment_msg = None
            comment_time = None
            comments_data = None
            try:
                with open(path + 'COMMENTS/' + event_id + '_comments.json', 'r') as comments_file:
                    comments_data = json.load(comments_file)
                    if (comments_data is not None) and \
                            (len(comments_data['data']) > 0):
                        for comment in comments_data['data']:
                            if 'message' not in comment:
                                continue  # Ignore comments with no text for our purpose

                            # Facebook's comment id is a string, we want ids to be integers so we
                            # generate our own sequential ids for comments.
                            comment_id = len(comments)  # Comment id, unique for each comment
                            comment_msg = comment['message']  # Comment message data
                            comment_time = comment['updated_time']  # Comment update time
                            comments[comment_id] = (comment_msg, comment_time, event_id)
            except:
                pass  # Silently ignore, some events have no comment files

            # Country codes are no longer retrieved by facebook.
            # We have to generate an id of our own instead..
            if (location_country not in countries) and (location_country is not None):
                country_id = len(countries)
                countries[location_country] = country_id

            # Some attributes are not assigned ids by facebook so we have to assign them by ourselves.
            # The first time we populate the database, we treat those names as "keys" that belong to the same
            # ids in the database. In reality, the moment we're done populating the database, these names are
            # no longer keys and users may add additional streets with similar names (but not the
            # same ids).
            country_id = countries[location_country] if location_country in countries else -1
            if (location_city not in cities) and (location_city is not None):
                city_id = len(cities)
                cities[location_city] = (city_id, country_id)

            city_id = cities[location_city][0] if location_city in cities else -1
            street_key = (country_id, city_id, location_street)
            if (street_key not in streets) and (location_street is not None):
                street_id = len(streets)
                streets[street_key] = (street_id, location_street, city_id)  # Assign sequential ids

            if (place_id not in places) and (place_id is not None):
                is_key_valid = location_street is not None
                street_id = streets[street_key][0] if is_key_valid else -1
                places[place_id] = (place_name, street_id, location_latitude, location_longitude)

            if (event_timezone not in timezones) and (event_timezone is not None):
                timezones[event_timezone] = len(timezones)  # Assign sequential ids

            if (event_owner_id not in owners) and (event_owner_id is not None):
                owners[event_owner_id] = event_owner_name

            timezone_id = timezones[event_timezone] if event_timezone in timezones else -1

            if event_id is not None:
                events[event_id] = (event_name,
                                    event_attending_count,
                                    event_declined_count,
                                    event_maybe_count,
                                    event_interested_count,
                                    event_noreply_count,
                                    event_is_canceled,
                                    event_description,
                                    event_category,
                                    event_can_guests_invite,
                                    cover_url,
                                    event_ticket_uri,
                                    event_guest_list_enabled,
                                    event_start_time,
                                    event_end_time,
                                    event_updated_time,
                                    timezone_id,
                                    event_type)

                if event_owner_id is not None:
                    event_owner_assoc[event_id] = event_owner_id

                if place_id is not None:
                    event_place_assoc[event_id] = place_id


def commit_dictionaries_to_db():
    """ Inserts all data in the dictionaries into the database """

    # Connect to Database..
    con = MySQLdb.connect(database_hostname, 'DbMysql08', 'DbMysql08', 'DbMysql08', charset='utf8')
    con.autocommit(False)
    with con:

        # ================================================================
        # ---- Database populated from this point onwards ----
        # ================================================================

        # Create cursor for executing INSERT queries..
        cur = con.cursor(MySQLdb.cursors.DictCursor)

        try:
            populate_categories(cur, con)  # Populate Category table
        except Exception as err:
            print('Error populating categories entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_countries(cur, con)
        except Exception as err:
            print('Error populating country entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_cities(cur, con)
        except Exception as err:
            print('Error populating city entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_streets(cur, con)
        except Exception as err:
            print('Error populating street entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_places(cur, con)
        except Exception as err:
            print('Error populating place entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_timezones(cur, con)
        except Exception as err:
            print('Error populating timezone entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_owners(cur, con)
        except Exception as err:
            print('Error populating owner entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_events(cur, con)
        except Exception as err:
            print('Error populating event entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_event_owner_association(cur, con)
        except Exception as err:
            print('Error populating event-owner association entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_event_place_association(cur, con)
        except Exception as err:
            print('Error populating event-place association entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_comments(cur, con)
        except Exception as err:
            print('Error populating comment entities')
            tb = traceback.format_exc()
            print(tb)

        con.close()
        print('Database population process done!')