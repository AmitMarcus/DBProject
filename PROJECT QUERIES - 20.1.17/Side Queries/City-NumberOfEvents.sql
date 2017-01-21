SELECT City.id AS City_ID,City.name AS City_Name ,Count(Event.id) As Num_Of_Events
FROM Event,Place,Event_Place,City,Street
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id=Street.id and Street.city_id=City.id
GROUP BY City.id,City.name
ORDER BY Num_Of_Events DESC;