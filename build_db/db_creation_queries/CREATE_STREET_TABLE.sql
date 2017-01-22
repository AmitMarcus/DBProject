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
ENGINE=MyISAM
;