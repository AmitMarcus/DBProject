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