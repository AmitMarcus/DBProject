SELECT 
    Owner.name AS owner_name,
    COUNT(Event.id) AS number_of_events
FROM
    Event,
    Owner,
    Event_Owner,
    Event_Desc_Search
WHERE
    Event.id = Event_Owner.event_id AND Event.id=Event_Desc_Search.event_id
        AND Event_Owner.owner_id = Owner.id
        AND (MATCH (Event_Desc_Search.description) AGAINST ('+Love' IN BOOLEAN MODE))
GROUP BY Owner.id
ORDER BY number_of_events DESC
LIMIT 10;
