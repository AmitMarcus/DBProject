SELECT Street.id AS Street_ID,Street.name AS Street_Name,City.name AS City_Name,Country.name AS Country_Name,Count(Event.id) AS NumOfEvents
FROM Event,Place,Event_Place,Street,City,Country
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id=Street.id 
		and Street.city_id=City.id and City.country_id=Country.id and (Country.name='United States' OR Country.name='United Kingdom')
GROUP BY Street.id,Street.name,City.name,Country.name
ORDER BY NumOfEvents DESC
LIMIT 5;