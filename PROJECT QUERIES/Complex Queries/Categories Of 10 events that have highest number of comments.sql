SELECT DISTINCT Category.id AS Category_ID,Category.name AS Category_Name
FROM Category,(SELECT Event.id AS EventID,Event.category_id AS EventCategoryID, COUNT(Comment.id) AS Num_Of_Comments
					FROM Event,Comment,Category
					WHERE Event.id=Comment.event_id and Event.category_id=Category.id and Category.name!='Misc'
					GROUP BY Event.id,Event.category_id
					ORDER BY Num_Of_Comments DESC
					LIMIT 10) AS TopTenEventsByComments
WHERE Category.id=TopTenEventsByComments.EventCategoryID