SELECT Category.id AS Category_ID,Category.name AS Category_Name, max(Event_Time.start_time) AS Max_Date
FROM Category,Event, Event_Time
WHERE Category.id=Event.category_id and Event.id=Event_Time.event_id
GROUP BY Category.id,Category.name
ORDER BY Max_Date DESC;