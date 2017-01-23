CREATE TABLE Event_Desc_Search (
	event_id BIGINT(20) NOT NULL,
	description VARCHAR(700)  DEFAULT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE='MyISAM'
;