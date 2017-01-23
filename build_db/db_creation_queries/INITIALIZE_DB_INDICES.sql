# PRIMARY keys are automatically indexed by MySQL, we optimize additional fields important to our queries

CREATE INDEX cityCountryIDIndex ON City(country_id);

CREATE INDEX streetCityIDIndext ON Street(city_id);

CREATE INDEX placeStreetIDIndext ON Place(street_id);

CREATE INDEX eventCategoryIDIndex ON Event(category_id);
CREATE FULLTEXT INDEX FullTextSearchIndex ON Event_Desc_Search(description);

CREATE INDEX eventGuestsAttendingCountIndex ON Event_Guests(attending_count);

CREATE INDEX eventTimeStartTimeIndex ON Event_Time(start_time);

CREATE INDEX CommentEventIDIndex ON Comment(event_id);

CREATE INDEX eventPlacePlaceIDIndex ON Event_Place(place_id);

CREATE INDEX eventOwnerOwnerIDIndex ON Event_Owner(owner_id);

