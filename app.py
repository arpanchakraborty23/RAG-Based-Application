from flask import Flask, request, jsonify, render_template
from src.cloud.s3_storege import S3Storage
from src.logging import logging
from langchain_community.vectorstores import FAISS
from src.pipline.retrieever_genaration_pipline import RetrieverGenaration
from src.pipline.preprocess_upload_doc_pipline import UploadDataToVectoreDb
import os
import mysql.connector

# Configure logging
logging.basicConfig(level=logging.INFO)

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
            "INSERT INTO chat_history (role, content, timestamp) VALUES (%s, %s, NOW())",
            (role, content),
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
        cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 10")
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

@app.route("/history", methods=["GET"])
def history():
    chat_history = fetch_chat_history()
    return jsonify(chat_history)

@app.route("/upload", methods=["POST"])
def upload_document():
    try:
        logging.info("Upload endpoint called")

        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Check file extension
        if not file.filename.endswith((".txt", ".pdf")):
            return jsonify({"error": "Only .txt and .pdf files are supported"}), 400

        # Process the new document Chunking and Storing
        obj=UploadDataToVectoreDb(file=file)
        obj.new_vectore_Db()

        return jsonify({
            "message": "File uploaded and added to FAISS successfully"
        })

    except Exception as e:
        logging.error(f"Error processing document: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/query", methods=["POST"])
def chat():
    try:
        query = request.json

        if 'question' not in query:
           return jsonify({'error': 'No question provided'}), 400

        logging.info(f'Query received: {query}')
        response = RetrieverGenaration().get_response(query=query['question'])
        logging.info(f'Response of query: {response}')

        # Store in MySQL
        # store_chat("user", query["question"])  # Fixed key
        # store_chat("system", response["result"])

        return jsonify({"answer": response})

    except Exception as e:
        logging.error(f"Error in retrieval: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
