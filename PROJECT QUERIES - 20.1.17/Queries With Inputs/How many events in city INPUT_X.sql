SELECT City.id AS City_ID,City.name AS City_Name, COUNT(Event.id) AS Number_Of_Events_At_City
FROM Event,Street,City,Place,Event_Place
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id = Street.id 
												and Street.city_id=City.id and City.name=X;