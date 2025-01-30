import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
from src.logging import logging


# MySQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": "chatdb",
    
}

def store_chat(role, content):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (role, content, timestamp) VALUES (%s, %s, NOW())",
            (role, content),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.info(f"Error storing chat: {e}")
        raise e

def fetch_chat_history():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 10")
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        return history
    except Exception as e:
        logging.error(f"Error fetching chat history: {e}")
        return []
    
# Test the function
if __name__ == "__main__":
    try:
        store_chat("user", "Hello, this is a test message!")
        print("Chat stored successfully.")
    except Exception as e:
        print(f"Test failed: {e}")