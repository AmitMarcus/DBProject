SELECT Owner.id AS Owner_ID, Owner.name AS Owner_Name,COUNT(Event.id) AS Number_Of_Events_With_Love
FROM Event,Owner,Event_Owner,Event_Desc_Search
WHERE Event.id=Event_Owner.event_id and Event_Owner.owner_id=Owner.id and (MATCH(Event_Desc_Search.description) AGAINST('+Love' IN BOOLEAN MODE))
                                    and Event.id=Event_Desc_Search.event_id
GROUP BY Owner.id
ORDER BY Number_Of_Events_With_Love DESC
LIMIT 10;
