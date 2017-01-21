CREATE INDEX categoryIdIndex ON Category(id);

CREATE INDEX timeZoneIdIndex ON Timezone(id);

CREATE INDEX countryIDIndex ON Country(id);

CREATE INDEX cityIdIndex ON City(id);
CREATE INDEX cityCountryIDIndex ON City(country_id);

CREATE INDEX streetIdIndex ON Street(id);
CREATE INDEX streetCityIDIndext ON Street(city_id);

CREATE INDEX placeIdIndex ON Place(id);
CREATE INDEX placeStreetIDIndext ON Place(street_id);

CREATE INDEX ownerIdIndex ON Owner(id);

CREATE INDEX eventIdIndex ON Event(id);
CREATE INDEX eventCategoryIDIndex ON Event(category_id);
CREATE FULLTEXT INDEX FullTextSearchIndex (description);

CREATE INDEX eventGuestsIdIndex ON Event_Guests(event_id);
CREATE INDEX eventGuestsAttendingCountIndex ON Event_Guests(attending_count);

CREATE INDEX eventTimeEventIdIndex ON Event_Time(event_id);
CREATE INDEX eventTimeStartTimeIndex ON Event_Time(start_time);

CREATE INDEX eventOwnerOwnerIDIndex ON Event_Owner(owner_id);

CREATE INDEX eventPlacePlaceIDIndex ON Event_Place(place_id);

CREATE INDEX CommentIdIndex ON Comment(id);
CREATE INDEX CommentEventIDIndex ON Comment(event_id);