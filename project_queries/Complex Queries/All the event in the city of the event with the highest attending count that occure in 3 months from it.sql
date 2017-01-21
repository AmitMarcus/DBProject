SELECT Event.id AS Event_ID, Event.name AS Event_Name, Category.name AS Event_Category,City.name AS City_Name,Event.description, Event_Time.start_time, Event_Time.end_time
FROM Event,Category,Place,Event_Place,Street,City,Event_Time,(SELECT Month(EventTime1.start_time) AS monthOfHighestAtt,City1.id AS cityID, EventGuests1.attending_count as maxAtt
																					FROM Event as Event1,Place AS Place1,Event_Place AS EventPlace1, Street AS Street1, City As City1, Event_Time AS EventTime1, Event_Guests AS EventGuests1
																					WHERE Event1.id=EventTime1.event_id and Event1.id=EventGuests1.event_id 
																								and Event1.id=EventPlace1.event_id and EventPlace1.place_id=Place1.id and Place1.street_id = Street1.id and Street1.city_id = City1.id
																					ORDER BY (maxAtt) DESC
																					LIMIT 1) AS maxAttTable
WHERE Event.category_id=Category.id and Event.id=Event_Place.event_id and Event_Place.place_id = Place.id and Place.street_id = Street.id and Street.city_id = City.id and City.id = maxAttTable.cityID
and Event.id=Event_Time.event_id and ABS(Month(Event_Time.start_time)-maxAttTable.monthOfHighestAtt)<=3;