SELECT 
    Owner.name AS owner_name,
    COUNT(Event.id) AS number_of_events
FROM
    Event,
    Owner,
    Event_Owner
WHERE
    Event.id = Event_Owner.event_id
        AND Event_Owner.owner_id = Owner.id
        AND (MATCH (Event.description) AGAINST ('+Love' IN BOOLEAN MODE))
GROUP BY Owner.id
ORDER BY Number_Of_Events_With_Love DESC
LIMIT 10;