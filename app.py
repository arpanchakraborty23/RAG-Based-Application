from flask import Flask, request, jsonify,render_template
from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from flask_cors import CORS
from langchain.chains import RetrievalQA
from src.pipline.retrieever_genaration_pipline import RetrieverGenaration
from dotenv import load_dotenv
import os
import mysql.connector
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MySQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
}

# Store chat history in MySQL
def store_chat(role, content):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (role, content) VALUES (%s, %s)",
            (role, content)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error storing chat: {e}")

# Retrieve chat history
def fetch_chat_history():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 10")
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        return history
    except Exception as e:
        logging.error(f"Error fetching chat history: {e}")
        return []
@app.route('/')
def index():
    return render_template('index.html')

# API Endpoint: Chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    response = RetrieverGenaration(query=query)
    
    # Store in MySQL
    store_chat("user", query)
    store_chat("system", response["result"])

    return jsonify({"answer": response["result"]})

# API Endpoint: Chat History
@app.route("/history", methods=["GET"])
def history():
    chat_history = fetch_chat_history()
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
