#returns the comments of the event with id equals to the input id.

SELECT 
    message,
    DATE_FORMAT(updated_time, '%%e/%%c/%%Y %%H:%%i') AS message_updated_time
FROM
    Comment
WHERE
    event_id = %s
ORDER BY updated_time DESC
