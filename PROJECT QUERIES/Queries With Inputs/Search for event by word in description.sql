SELECT Event.id AS Event_ID,Event.name AS Event_Name, Category.name AS Category_Name,
									Country.name AS Country_Name,City.name AS City_Name, 
									Street.name AS Street_Name,Event.description AS Event_Description
FROM Event,Event_Place,Place,Country,City,Street,Category
WHERE Event.id=Event_Place.event_id and Event_Place.place_id = Place.id and Place.street_id=Street.id 
				and Street.city_id=City.id and City.country_id=Country.id 
				and Event.category_id=Category.id and MATCH(Event.description) AGAINST('+word' IN BOOLEAN MODE)
