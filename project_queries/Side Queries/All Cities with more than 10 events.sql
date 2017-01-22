SELECT City.id, City.name
FROM City
JOIN Street
ON Street.city_id = City.id
JOIN Place
ON Street.id = Place.street_id
JOIN Event_Place
ON Event_Place.place_id = Place.id
GROUP BY City.id
HAVING COUNT(Event_Place.event_id) >= 10
ORDER BY COUNT(Event_Place.event_id) DESC
