SELECT Event.id AS Event_ID,Event.name AS Event_Name,Category.name AS Category_Name,Event_Time.start_time AS Event_Start_Time,Event.description AS Event_Description
FROM Event,Category,Event_Time,(SELECT min(Event2.id) AS Newest_Event_ID
											FROM Event AS Event2,Event_Time AS EventTime2,(SELECT Cat1.id AS CategoryID, max(EventTime1.start_time) AS maxDate
																											FROM Category AS Cat1 ,Event AS Event1, Event_Time AS EventTime1
																											WHERE Cat1.id=Event1.category_id and Event1.id=EventTime1.event_id
																											GROUP BY CategoryID
																											ORDER BY maxDate DESC
																											LIMIT 8) AS CatMaxDateTable
											WHERE Event2.category_id=CatMaxDateTable.CategoryID and Event2.id=EventTime2.event_id and EventTime2.start_time=CatMaxDateTable.maxDate
											GROUP BY Event2.category_id) AS EventIDS
WHERE Event.id=EventIDS.Newest_Event_ID and Event.category_id=Category.id and Event.id=Event_Time.event_id;