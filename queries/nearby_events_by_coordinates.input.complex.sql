# Search for events within distance of 4 km of the location (search_lat, search_log)
SELECT 
    Event.id AS event_id,
    Event.name as event_name,
    Category.name as event_category,
    Place.name AS place_name,
    City.name AS city,
    Street.name AS street,
    # 6371 is a constant used to fetch kilometers for this formula
    ROUND((6371 * ACOS(COS(RADIANS(%s)) * COS(RADIANS(Place.latitude)) * COS(RADIANS(Place.longitude) - RADIANS(%s)) + SIN(RADIANS(%s)) * SIN(RADIANS(Place.latitude)))), 2) AS distance,
    latitude,
    longitude
FROM
    Place
        JOIN
    Street ON Street.id = Place.street_id
        JOIN
    City ON City.id = Street.city_id
		JOIN
	Event_Place ON Event_Place.place_id = Place.id
		JOIN
	Event ON Event.id = Event_Place.event_id
		JOIN
	Category ON Category.id = Event.category_id
HAVING distance > 0 AND distance < 4
ORDER BY distance
LIMIT 26;