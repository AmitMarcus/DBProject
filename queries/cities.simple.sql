SELECT 
    City.id AS city_id,
    City.name AS city,
    Country.name AS country
FROM
    City,
    Country
WHERE
    Country.id = City.country_id
ORDER BY Country.name, City.name