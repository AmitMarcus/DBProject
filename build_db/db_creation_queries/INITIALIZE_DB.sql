DROP TABLE IF EXISTS DbMysql08.GlobalMessage;

DROP TABLE IF EXISTS DbMysql08.Comment;

DROP TABLE IF EXISTS DbMysql08.Event_Desc_Search;
DROP TABLE IF EXISTS DbMysql08.Event_Place;
DROP TABLE IF EXISTS DbMysql08.Event_Owner;
DROP TABLE IF EXISTS DbMysql08.Event_Time;
DROP TABLE IF EXISTS DbMysql08.Event_Guests;
DROP TABLE IF EXISTS DbMysql08.Event;

DROP TABLE IF EXISTS DbMysql08.Owner;

DROP TABLE IF EXISTS DbMysql08.Timezone;

DROP TABLE IF EXISTS DbMysql08.Place;

DROP TABLE IF EXISTS DbMysql08.Street;

DROP TABLE IF EXISTS DbMysql08.City;

DROP TABLE IF EXISTS DbMysql08.Country;

DROP TABLE IF EXISTS DbMysql08.Category;

CREATE TABLE Category 
(
	id SMALLINT(5) NOT NULL AUTO_INCREMENT,
	name VARCHAR(15) NOT NULL,
	PRIMARY KEY (id)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB';

CREATE TABLE Timezone 
(
	id MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
	timezone VARCHAR(40) NOT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Country 
(
	id SMALLINT(5) NOT NULL AUTO_INCREMENT,
	name VARCHAR(27) NOT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE City 
(
	id MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
	name VARCHAR(38) NOT NULL,
	country_id SMALLINT(5) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) 
        	   REFERENCES  Country(id),
	CHECK (id > -1),
	CHECK (country_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Street 
(
	id MEDIUMINT(8) NOT NULL,
	name VARCHAR(120) NOT NULL,
	city_id MEDIUMINT(8) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (city_id)
		REFERENCES City(id),
	CHECK (id > -1),
	CHECK (city_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Place 
(
	id BIGINT(20) NOT NULL,
	name VARCHAR(50) NOT NULL,
	street_id MEDIUMINT(8) DEFAULT -1,
	latitude DOUBLE DEFAULT NULL,
	longitude DOUBLE DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (street_id)
		REFERENCES Street(id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Owner 
(
	id BIGINT(20) NOT NULL,
	name VARCHAR(27) NOT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event (
	id BIGINT(20) NOT NULL,
	name VARCHAR(100)  NOT NULL,
	is_canceled Tinyint(1)  DEFAULT 0,
	category_id SMALLINT(5)  DEFAULT 999,
	can_guest_invite Tinyint(1)  DEFAULT 0,
	cover_source VARCHAR(255)  DEFAULT NULL,
	event_ticket_uri VARCHAR(600) DEFAULT NULL,
	guest_list_enabled Tinyint(1)  DEFAULT 1,
	event_type VARCHAR(12)  DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category_id)
		REFERENCES Category(id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event_Guests
 (
	event_id BIGINT(20) NOT NULL,
	attending_count MEDIUMINT(8) NOT NULL,
	declined_count MEDIUMINT(8) NOT NULL,
	maybe_count MEDIUMINT(8)  NOT NULL,
	interested_count MEDIUMINT(8)  DEFAULT NULL,
	noreply_count MEDIUMINT(8)  NOT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	CHECK (attending_count >= 0),
	CHECK (declined_count >= 0),
	CHECK (maybe_count >= 0),
	CHECK (interested_count >= 0),
	CHECK (noreply_count >= 0),
	CHECK (event_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event_Time 
(
	event_id BIGINT(20) NOT NULL,
	timezone_id MEDIUMINT(8)  DEFAULT NULL,
	start_time DATETIME  NOT NULL,
	end_time DATETIME  NOT NULL,
	update_time DATETIME  DEFAULT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (timezone_id)
		REFERENCES Timezone(id),
	CHECK (update_time <= NOW()),
	CHECK (end_time >= start_time),
	CHECK (event_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event_Owner (
	event_id BIGINT(20) NOT NULL,
	owner_id BIGINT(20) NOT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (owner_id)
		REFERENCES Owner(id),
	CHECK (event_id > -1),
	CHECK (owner_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event_Place (
	event_id BIGINT(20) NOT NULL,
	place_id BIGINT(20) NOT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (place_id)
		REFERENCES Place(id),
	CHECK (event_id > -1),
	CHECK (place_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE Event_Desc_Search (
	event_id BIGINT(20) NOT NULL,
	description VARCHAR(700)  DEFAULT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='MyISAM'
;

CREATE TABLE Comment 
(
	id BIGINT(20) NOT NULL AUTO_INCREMENT,
	message VARCHAR(700) NOT NULL,
	updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	event_id BIGINT(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),

	CHECK (updated_time <= NOW()),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;

CREATE TABLE GlobalMessage 
(
	id BIGINT(20) NOT NULL AUTO_INCREMENT,
	message VARCHAR(90) NOT NULL,
	fullname VARCHAR(27) NOT NULL,
	post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	city_id MEDIUMINT(8) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (city_id)
		REFERENCES City(id),
	CHECK (id > -1),
	CHECK (city_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='InnoDB'
;