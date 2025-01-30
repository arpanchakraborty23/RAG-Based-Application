CREATE DATABASE chat_history;

USE chat_history;

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role ENUM('user', 'system') NOT NULL,
    content TEXT NOT NULL
);
