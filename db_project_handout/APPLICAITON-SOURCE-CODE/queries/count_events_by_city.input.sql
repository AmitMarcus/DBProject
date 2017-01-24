#returns the number of events that occurs in the city with id equals to the input city's id.

SELECT 
    City.name AS city,
    Country.name AS country,
    COUNT(Event.id) AS number_of_events
FROM
    Event,
    Street,
    City,
    Country,
    Place,
    Event_Place
WHERE
    Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.country_id = Country.id
        AND City.id = %s
