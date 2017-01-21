CREATE INDEX eventIdIndex ON Event(id);
CREATE INDEX eventCategoryIDIndex ON Event(category_id);
CREATE FULLTEXT INDEX FullTextSearchIndex ON Event(description);