# -- All events in hottest season in the city of the biggest event --
# Returns all events ordered by number of attendents in the city that hosts the event
# with the largest amount of attending people, and the city hosts at least 10 events total.
# The events returned must also occur within the same season as the event
# with the maximal amount of attendees
# (meaning 2 months before or after the maximal event, can occur on different years).
SELECT 
    Event.id AS Event_ID,
    Event.name AS Event_Name,
    Category.name AS Event_Category,
    City.name AS City_Name,
    Event.description,
    Event_Time.start_time,
    Event_Time.end_time,
    Event_Guests.attending_count
FROM
    Event,
    Category,
    Place,
    Event_Place,
    Street,
    City,
    Event_Time,
    Event_Guests,
    (SELECT 
        MONTH(EventTime1.start_time) AS monthOfHighestAtt,
            EventfulCities.id AS cityID,
            EventGuests1.attending_count AS maxAtt
    FROM
        Event AS Event1, Place AS Place1, Event_Place AS EventPlace1, Street AS Street1,
        Event_Time AS EventTime1, Event_Guests AS EventGuests1,
        (SELECT City.id
		 FROM City
		 JOIN Street ON Street.city_id = City.id
		 JOIN Place ON Street.id = Place.street_id
		 JOIN Event_Place ON Event_Place.place_id = Place.id
		 GROUP BY City.id
		 HAVING COUNT(Event_Place.event_id) >= 10) AS EventfulCities
    WHERE
        Event1.id = EventTime1.event_id
            AND Event1.id = EventGuests1.event_id
            AND Event1.id = EventPlace1.event_id
            AND EventPlace1.place_id = Place1.id
            AND Place1.street_id = Street1.id
            AND Street1.city_id = EventfulCities.id
    ORDER BY (maxAtt) DESC
    LIMIT 1) AS maxAttTable
WHERE
    Event.category_id = Category.id
        AND Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.id = maxAttTable.cityID
        AND Event.id = Event_Time.event_id
        AND Event_Guests.event_id = Event.id
        AND ABS(MONTH(Event_Time.start_time) - maxAttTable.monthOfHighestAtt) <= 2
ORDER BY Event_Guests.attending_count DESC;