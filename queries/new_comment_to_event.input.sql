#Insert new comment according to message and event_id as inputs to our Comment table



INSERT INTO Comment (message, event_id) VALUES (%s, %s)
