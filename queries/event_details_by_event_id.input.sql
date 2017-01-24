SELECT 
    Event.id AS event_id,
    Event.name AS event_name,
    Event_Desc_Search.description AS event_description,
    Owner.name AS owner,
    country,
    city,
    street,
    latitude,
    longitude,
    is_canceled,
    cover_source,
    event_ticket_uri,
    maybe_count,
    noreply_count,
    attending_count,
    declined_count,
    interested_count,
    DATE_FORMAT(Event_Time.start_time,
            '%%e/%%c/%%Y %%H:%%i') AS event_start_time,
    DATE_FORMAT(Event_Time.end_time,
            '%%e/%%c/%%Y %%H:%%i') AS event_end_time,
    Category.name AS event_category,
     DATE_FORMAT(update_time,
            '%%e/%%c/%%Y %%H:%%i') AS update_time,
	Timezone.timezone as timezone
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
            AND City.country_id = Country.id) Place ON Place.event_id = Event.id
        LEFT OUTER JOIN
    Event_Guests ON Event.id = Event_Guests.event_id
        LEFT OUTER JOIN
    Event_Time ON Event.id = Event_Time.event_id
            LEFT OUTER JOIN
    Timezone ON Timezone.id = Event_Time.timezone_id,
    Event_Desc_Search,
    Event_Owner,
    Owner,
    Category
WHERE
    Event.id = %s
        AND Event.id = Event_Desc_Search.event_id
        AND Event.id = Event_Owner.event_id
        AND Owner.id = Event_Owner.owner_id
        AND Event.category_id = Category.id