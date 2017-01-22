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
