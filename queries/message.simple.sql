SELECT 
    message,
    fullname,
    City.id AS city_id,
    City.name AS city,
    Country.name AS country,
    DATE_FORMAT(post_time, '%e/%c/%Y %H:%i') AS post_time
FROM
    GlobalMessage,
    City,
    Country
WHERE
    Country.id = City.country_id
        AND GlobalMessage.city_id = City.id
ORDER BY post_time DESC
LIMIT 1