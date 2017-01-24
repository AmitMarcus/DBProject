This tool uses facebook graph api 2.2 to download events and comments data and populate our
MYSQL DBMS..

Usage:

python db_extract download_data // Harvests selected events from facebook to local Json files
python db_extract populate_db   // Populates DB with data stored in Json files

- Please run using Python 2.7 - 
The library uses the following dependencies:
1) facebook-sdk version 2.00 (installed on Nova)
2) MySQLDb (installed on Nova)


Note:
We use Facebook's user_token to fetch event ids from facebook (even public events require user_token).
app_token is the "password" we use to fetch data about the events themselves (the fields, comments..).

Retrival tool uses both tokens.
The Server uses only the app_token (updates certain fields of events)..

Retrival tool stores data in Jsons first so we can make use of it again in case something bad happens in the database during development (this helped us keep track of the data we dealt with during development).