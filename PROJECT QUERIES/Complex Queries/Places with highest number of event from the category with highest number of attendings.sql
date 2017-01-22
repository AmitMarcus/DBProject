SELECT Place.id AS Place_ID, Place.name AS Place_Name, Country.name AS Country_Name, City.name AS City_Name, Street.name AS Street_Name, COUNT(Event.id) AS NumberOfEvents
FROM Place AS Place,Street,City,Country,Event,Event_Place,(SELECT Category1.id AS CategoryID, SUM(EventGuests1.attending_count) AS Num_Of_Attendings
																	FROM Event AS Event1 ,Category AS Category1, Event_Guests AS EventGuests1
																	WHERE Event1.category_id=Category1.id and Event1.id=EventGuests1.event_id and Category1.name!='Misc'
																	GROUP BY Category1.id
																	ORDER BY Num_Of_Attendings DESC
																	LIMIT 1) AS Category_With_Highest_Att
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id=Street.id and Street.city_id=City.id 
												and City.country_id=Country.id and Event.category_id=Category_With_Highest_Att.CategoryID
GROUP BY Place.id
ORDER BY(NumberOfEvents) DESC
LIMIT 10;