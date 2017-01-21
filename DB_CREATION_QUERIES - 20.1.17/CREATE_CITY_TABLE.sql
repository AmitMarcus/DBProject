CREATE TABLE City 
(
	id MEDIUMINT(10) NOT NULL AUTO_INCREMENT,
	name VARCHAR(38) NOT NULL,
	country_id MEDIUMINT(10) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) 
        	   REFERENCES  Country(id) 
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;
