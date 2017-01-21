CREATE TABLE Event_Guests
 (
	event_id BIGINT(20) NOT NULL,
	attending_count MEDIUMINT(8) NOT NULL,
	declined_count MEDIUMINT(8) NOT NULL,
	maybe_count MEDIUMINT(8)  NOT NULL,
	interested_count MEDIUMINT(8)  DEFAULT NULL,
	noreply_count MEDIUMINT(8)  NOT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	CHECK (attending_count >= 0),
	CHECK (declined_count >= 0),
	CHECK (maybe_count >= 0),
	CHECK (interested_count >= 0),
	CHECK (noreply_count >= 0)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;