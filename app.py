from flask import Flask, request, jsonify, render_template
from src.cloud.s3_storege import S3Storage
from src.logging import logging
from langchain_community.vectorstores import FAISS
from src.pipline.retrieever_genaration_pipline import RetrieverGenaration
from src.pipline.preprocess_upload_doc_pipline import UploadDataToVectoreDb
import os
from sql_connection import fetch_chat_history,store_chat



app = Flask(__name__)

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
        
        S3Storage().upload_file(
            file_obj=file,
            filename=file.filename
        )

        # Process the new document Chunking and Storing
        obj=UploadDataToVectoreDb()
        chunks=obj.process_document(file=file)
        obj.vector_store(chunks=chunks)

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

        if "question" not in query:
            return jsonify({"error": "No question provided"}), 400

        user_question = query["question"]
        logging.info(f"Query received: {user_question}")

        # Get response from RAG model
        response = RetrieverGenaration().get_response(query=user_question)
        system_answer = response if isinstance(response, str) else response.get("result", "")

        logging.info(f"Response of query: {system_answer}")

        # Store chat history in MySQL
        store_chat("user", user_question)   # Store user question
        store_chat("system", system_answer) # Store system response

        return jsonify({"answer": system_answer})

    except Exception as e:
        logging.error(f"Error in retrieval: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
