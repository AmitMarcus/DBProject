CREATE TABLE Event (
	id BIGINT(20) NOT NULL,
	name VARCHAR(100)  NOT NULL,
	is_canceled Tinyint(1)  DEFAULT 0,
	description VARCHAR(700)  DEFAULT NULL,
	category_id SMALLINT(5)  DEFAULT 999,
	can_guest_invite Tinyint(1)  DEFAULT 0,
	cover_source VARCHAR(255)  DEFAULT NULL,
	event_ticket_uri VARCHAR(600) DEFAULT NULL,
	guest_list_enabled Tinyint(1)  DEFAULT 1,
	event_type VARCHAR(12)  DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category_id)
		REFERENCES Category(id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;