CREATE TABLE Comment 
(
	id BIGINT(20) NOT NULL AUTO_INCREMENT,
	message VARCHAR(700) NOT NULL,
	updated_time DATETIME DEFAULT NULL,
	event_id BIGINT(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),

	CHECK (updated_time <= CURTIME()),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;