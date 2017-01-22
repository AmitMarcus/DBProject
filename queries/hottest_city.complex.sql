SELECT 
    City.name AS city_name,
    Event.id AS event_id,
    Event.name AS event_name,
    Category.name AS event_category,
    Event.description AS event_description,
    DATE_FORMAT(Event_Time.start_time, '%e/%c/%Y %H:%i') AS event_start_time,
    DATE_FORMAT(Event_Time.end_time, '%e/%c/%Y %H:%i') AS event_end_time
FROM
    Event,
    Street,
    City,
    Category,
    Place,
    Event_Place,
    Event_Time,
    (SELECT 
        City1.id AS CityId1, COUNT(Event1.id) AS Num_Of_Events
    FROM
        Event AS Event1, Place AS Place1, Event_Place AS EventPlace1, Street AS Street1, City AS City1
    WHERE
        Place1.street_id = Street1.id
            AND Street1.city_id = City1.id
            AND Event1.id = EventPlace1.event_id
            AND EventPlace1.place_id = Place1.id
    GROUP BY City1.id
    ORDER BY Num_Of_Events DESC
    LIMIT 1) AS CityMaxEventsTable
WHERE
    Event.category_id = Category.id
        AND Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.id = CityMaxEventsTable.CityId1
        AND Event.id = Event_Time.event_id
        AND Event_Time.start_time >= CURDATE()
ORDER BY (Event_Time.start_time)
LIMIT 10;