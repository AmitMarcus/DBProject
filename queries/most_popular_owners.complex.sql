SELECT 
    Owner.id AS owner_id,
    Owner.name AS owner_name,
    OwnerAttTable.OwnerAttendings AS owner_event_attendings,
    COUNT(Comment.id) AS number_of_comments
FROM
    Owner,
    Event,
    Event_Owner,
    Comment,
    (SELECT 
        Owner1.id AS OwnerID1,
            SUM(EventGuests1.attending_count) AS OwnerAttendings
    FROM
        Event AS Event1, Owner AS Owner1, Event_Owner AS EventOwner1, Event_Guests AS EventGuests1
    WHERE
        Event1.id = EventOwner1.event_id
            AND EventOwner1.owner_id = Owner1.id
            AND Event1.id = EventGuests1.event_id
    GROUP BY Owner1.id
    ORDER BY OwnerAttendings DESC
    LIMIT 20) AS OwnerAttTable
WHERE
    Event.id = Event_Owner.event_id
        AND Event_Owner.owner_id = Owner.id
        AND Owner.id = OwnerAttTable.OwnerID1
        AND Event.id = Comment.event_id
GROUP BY Owner.id , Owner.name , OwnerAttTable.OwnerAttendings
ORDER BY number_of_comments DESC
LIMIT 10;