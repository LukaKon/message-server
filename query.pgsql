SELECT 'from';
SELECT users.id,users.username, messages.message,messages.creation_date, messages.id FROM messages
JOIN users ON messages.from_id=users.id;

SELECT 'to';
SELECT users.id, users.username, messages.message,messages.creation_date, messages.id FROM messages
JOIN users ON messages.to_id=users.id;




SELECT DISTINCT users.id, users.username, messages.message
FROM users
JOIN messages ON users.id=messages.from_id;

SELECT DISTINCT ON (messages.creation_date) users.username, users.id , messages.message, messages.creation_date
            FROM users
            JOIN messages ON users.id=messages.from_id
            WHERE users.id=1;

select * from users;

drop database message_server;