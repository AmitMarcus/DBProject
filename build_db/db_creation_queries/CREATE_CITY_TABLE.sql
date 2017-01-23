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