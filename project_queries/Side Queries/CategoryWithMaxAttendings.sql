SELECT Category.id AS Category_ID,Category.name AS Category_Name, SUM(Event_Guests.attending_count) AS Num_Of_Attendings
FROM Event,Category,Event_Guests
WHERE Event.category_id=Category.id and Event.id=Event_Guests.event_id and Category.name!='Misc'
GROUP BY Category.id,Category.name
ORDER BY Num_Of_Attendings DESC
LIMIT 1;