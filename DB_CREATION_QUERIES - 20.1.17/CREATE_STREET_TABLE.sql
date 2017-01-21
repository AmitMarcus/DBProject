CREATE TABLE Street 
(
	id MEDIUMINT(10) NOT NULL,
	name VARCHAR(120) NOT NULL,
	city_id MEDIUMINT(10) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (city_id)
		REFERENCES City(id)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;