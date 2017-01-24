#query for the list of cities in countries order by country's name and city's name

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
