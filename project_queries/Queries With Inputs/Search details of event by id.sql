SELECT 
    Event.id,
    Event.name AS event_name,
    Event_Desc_Search.description AS Event_Description,
    Owner.name AS owner_name,
    country,
    city,
    street,
    latitude,
    longitude,
    is_canceled,
    cover_source,
    event_ticket_uri,
    Event_Guests.*
FROM
    Event
        LEFT OUTER JOIN
    (SELECT 
        event_id,
            Country.name AS country,
            City.name AS city,
            Street.name AS street,
            latitude,
            longitude
    FROM
        Event_Place, Country, City, Street, Place
    WHERE
        Event_Place.place_id = Place.id
            AND Place.street_id = Street.id
            AND Street.city_id = City.id
            AND City.country_id = Country.id) Place ON Place.event_id = Event.id,
    Event_Desc_Search,
    Event_Owner,
    Owner,
    Event_Guests
WHERE
    Event.id IN (1198513943527973 , 1398815377046293)
        AND Event.id = Event_Desc_Search.event_id
        AND Event.id = Event_Owner.event_id
        AND Owner.id = Event_Owner.owner_id
        AND Event.id = Event_Guests.event_id