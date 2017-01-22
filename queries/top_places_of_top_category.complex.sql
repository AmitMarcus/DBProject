SELECT 
    Place.name AS place_name,
    Country.name AS country,
    City.name AS city,
    Street.name AS street,
    COUNT(Event.id) AS number_of_events
FROM
    Place AS Place,
    Street,
    City,
    Country,
    Event,
    Event_Place,
    (SELECT 
        Category1.id AS CategoryID,
            SUM(EventGuests1.attending_count) AS Num_Of_Attendings
    FROM
        Event AS Event1, Category AS Category1, Event_Guests AS EventGuests1
    WHERE
        Event1.category_id = Category1.id
            AND Event1.id = EventGuests1.event_id
            AND Category1.name != 'Misc'
    GROUP BY Category1.id
    ORDER BY Num_Of_Attendings DESC
    LIMIT 1) AS Category_With_Highest_Att
WHERE
    Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.country_id = Country.id
        AND Event.category_id = Category_With_Highest_Att.CategoryID
GROUP BY Place.id
ORDER BY (number_of_events) DESC
LIMIT 10;