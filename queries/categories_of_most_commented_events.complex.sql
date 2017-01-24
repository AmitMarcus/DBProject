
--The categories of the 10 events with the highest number of comments

SELECT DISTINCT
    Category.name AS category
FROM
    Category,
    (SELECT 
        Event.id AS EventID,
            Event.category_id AS EventCategoryID,
            COUNT(Comment.id) AS Num_Of_Comments
    FROM
        Event, Comment, Category
    WHERE
        Event.id = Comment.event_id
            AND Event.category_id = Category.id
            AND Category.name != 'Misc'
    GROUP BY Event.id , Event.category_id
    ORDER BY Num_Of_Comments DESC
    LIMIT 10) AS TopTenEventsByComments
WHERE
    Category.id = TopTenEventsByComments.EventCategoryID
