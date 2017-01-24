
#Among all the streets in USA and UK, who are the 5 streets that got the highest number of events.



SELECT
    Street.name AS street,
    City.name AS city,
    Country.name AS country,
    COUNT(Event.id) AS number_of_events
FROM
    Event,
    Place,
    Event_Place,
    Street,
    City,
    Country
WHERE
    Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.country_id = Country.id
        AND (Country.name = 'United States'
        OR Country.name = 'United Kingdom')
GROUP BY Street.id , Street.name , City.name , Country.name
ORDER BY number_of_events DESC
LIMIT 5;
