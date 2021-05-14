SELECT 'from';
SELECT users.id,users.username, messages.message,messages.creation_date, messages.id FROM messages
JOIN users ON messages.from_id=users.id;

SELECT 'to';
SELECT users.id, users.username, messages.message,messages.creation_date, messages.id FROM messages
JOIN users ON messages.to_id=users.id;
