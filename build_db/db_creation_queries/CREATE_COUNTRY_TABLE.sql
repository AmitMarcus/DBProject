CREATE TABLE Country 
(
	id MEDIUMINT(10) NOT NULL AUTO_INCREMENT,
	name VARCHAR(27) NOT NULL,
	PRIMARY KEY (id),
	CHECK (id > -1)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;
