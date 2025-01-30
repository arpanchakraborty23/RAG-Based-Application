CREATE DATABASE IF NOT EXISTS chatdb;
USE chatdb;

CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role ENUM('user', 'system'),
    content TEXT
);
