CREATE TABLE Owner 
(
	id BIGINT(20) NOT NULL,
	name VARCHAR(27) NOT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;