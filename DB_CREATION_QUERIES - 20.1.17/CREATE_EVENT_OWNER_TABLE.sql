CREATE TABLE Event_Owner (
	event_id BIGINT(20) NOT NULL,
	owner_id BIGINT(20) NOT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (owner_id)
		REFERENCES Owner(id)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;