CREATE TABLE Event_Time 
(
	event_id BIGINT(20) NOT NULL,
	timezone_id MEDIUMINT(10)  DEFAULT NULL,
	start_time DATETIME  NOT NULL,
	end_time DATETIME  NOT NULL,
	update_time DATETIME  DEFAULT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (timezone_id)
		REFERENCES Timezone(id),
	CHECK (update_time <= CURTIME()),
	CHECK (end_time >= start_time)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;