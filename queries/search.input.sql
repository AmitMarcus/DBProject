SELECT 
    Event.id AS event_id,
    Event.name AS event_name,
    Category.name AS event_category,
    Country.name AS country,
    City.name AS city,
    Street.name AS street,
    Event.description AS event_description
FROM
    Event,
    Event_Place,
    Place,
    Country,
    City,
    Street,
    Category
WHERE
    Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.country_id = Country.id
        AND Event.category_id = Category.id
        AND MATCH (Event.description) AGAINST (+%s IN BOOLEAN MODE)
