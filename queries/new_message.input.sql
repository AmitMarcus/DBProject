#Insert new message according to message,fullname and city_id as inputs into our GlobalMessage table.

INSERT INTO GlobalMessage (message, fullname, city_id) VALUES (%s, %s, %s)
