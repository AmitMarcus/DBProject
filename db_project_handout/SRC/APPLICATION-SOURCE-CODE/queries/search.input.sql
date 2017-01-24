#Returns details of event (from some tables) that has the input word as a word
#in it's description


SELECT 
    Event.id AS event_id,
    Event.name AS event_name,
    Category.name AS event_category,
    Country.name AS country,
    City.name AS city,
    Street.name AS street,
    Event_Desc_Search.description AS event_description
FROM
    Event,
    Event_Place,
    Place,
    Country,
    City,
    Street,
    Category,
    Event_Desc_Search
WHERE
    Event.id = Event_Place.event_id
        AND Event_Place.place_id = Place.id
        AND Place.street_id = Street.id
        AND Street.city_id = City.id
        AND City.country_id = Country.id
        AND Event.category_id = Category.id
        AND Event.id = Event_Desc_Search.event_id
        AND MATCH (Event_Desc_Search.description) AGAINST (+%s IN BOOLEAN MODE)
