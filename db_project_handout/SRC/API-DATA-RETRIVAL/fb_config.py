# -*- coding: utf-8 -*-

""" Contains all configuration parameters for dealing with facebook-sdk and connection to mysql dbms"""
""" This is the configuration file used by the fb_extract script (the server connects using it's own parameters) """

# Get access token from: https://developers.facebook.com/tools/debug/accesstoken/
# Note: The app uses only the app_token!
# We used the user_key only in the db population tool (fb_extract) to fetch more interesting Events
# which were designated by facebook as private (we don't distinguish between facebook private and public events)
user_token = 'EAACtNKrCNh8BAPnr7PyzbBaJcwNq4ZA9h3KCGSRGXZBDbJZAZCt3pvWPcmWhjiz3KToTcZBv6zO4ttZCZCLZAElmaTiyQ93kg55kVqhZAVI4A0ko9VEZBmz12eykuwdUX2247W1jeVCC3BpwkBoIgE61ZA7GSYuN8ElSiMZD'
app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'

# For NOVA use: 'mysqlsrv.cs.tau.ac.il'
# Depending on where you run your script...
database_hostname = 'localhost'

# A mapping between Facebook Graph API Category ENUMS to our own app's category_id
categories = {
                'BOOK_EVENT': (1, 'Books'),
                'MOVIE_EVENT': (2, 'Movies'),
                'FUNDRAISER': (3, 'Fund Raising'),
                'VOLUNTEERING': (4, 'Volunteering'),
                'FAMILY_EVENT': (5, 'Family Event'),
                'FESTIVAL_EVENT': (6, 'Festival'),
                'NEIGHBORHOOD': (7, 'Neighborhood'),
                'RELIGIOUS_EVENT': (8, 'Religious'),
                'SHOPPING': (9, 'Shopping'),
                'COMEDY_EVENT': (10, 'Comedy'),
                'MUSIC_EVENT': (11, 'Music'),
                'DANCE_EVENT': (12, 'Dancing'),
                'NIGHTLIFE': (13, 'Nightlife'),
                'THEATER_EVENT': (14, 'Theater'),
                'DINING_EVENT': (15, 'Dining'),
                'FOOD_TASTING': (16, 'Food'),
                'CONFERENCE_EVENT': (17, 'Conference'),
                'MEETUP': (18, 'Meetup'),
                'CLASS_EVENT': (19, 'Class Event'),
                'LECTURE': (20, 'Lecture'),
                'WORKSHOP': (21, 'Workshop'),
                'FITNESS': (22, 'Fitness'),
                'SPORTS_EVENT': (23, 'Sports'),
                'ART_EVENT': (24, 'Art'),
                'OTHER': (999, 'Misc')
            }