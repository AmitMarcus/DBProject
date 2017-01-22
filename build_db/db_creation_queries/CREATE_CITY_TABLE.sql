CREATE TABLE City 
(
	id MEDIUMINT(10) NOT NULL AUTO_INCREMENT,
	name VARCHAR(38) NOT NULL,
	country_id MEDIUMINT(10) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) 
        	   REFERENCES  Country(id),
	CHECK (id > -1),
	CHECK (country_id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;
