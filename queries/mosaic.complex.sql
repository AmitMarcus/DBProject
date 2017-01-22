SELECT 
    Event.id AS event_id,
    Event.name AS event_name,
    Category.name AS event_category,
    Event.description AS event_description
FROM
    Event,
    Category,
    Event_Time,
    (SELECT 
        MIN(Event2.id) AS Newest_Event_ID
    FROM
        Event AS Event2, Event_Time AS EventTime2, (SELECT 
        Cat1.id AS CategoryID, MAX(EventTime1.start_time) AS maxDate
    FROM
        Category AS Cat1, Event AS Event1, Event_Time AS EventTime1
    WHERE
        Cat1.id = Event1.category_id
            AND Event1.id = EventTime1.event_id
    GROUP BY CategoryID
    ORDER BY maxDate DESC
    LIMIT 8) AS CatMaxDateTable
    WHERE
        Event2.category_id = CatMaxDateTable.CategoryID
            AND Event2.id = EventTime2.event_id
            AND EventTime2.start_time = CatMaxDateTable.maxDate
    GROUP BY Event2.category_id) AS EventIDS
WHERE
    Event.id = EventIDS.Newest_Event_ID
        AND Event.category_id = Category.id
        AND Event.id = Event_Time.event_id;