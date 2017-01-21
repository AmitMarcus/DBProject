CREATE TABLE Place 
(
	id BIGINT(20) NOT NULL,
	name VARCHAR(50) NOT NULL,
	street_id MEDIUMINT(10) DEFAULT NULL,
	latitude DOUBLE DEFAULT NULL,
	longitude DOUBLE DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (street_id)
		REFERENCES Street(id)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;
