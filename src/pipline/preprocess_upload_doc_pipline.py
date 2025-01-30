from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from src.config.config import TraningPiplineConfig
from src.logging import logging
import tempfile
import os

class UploadDataToVectoreDb:
    def __init__(self,file):
        self.traning_pipline=TraningPiplineConfig()
        self.file=file

    def process_document(self,file):
        try:
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, file.filename)
            file.save(temp_path)  # Save file temporarily

            # Load document based on type
            if file.filename.endswith('.pdf'):
                loader = PyPDFLoader(temp_path)
            elif file.filename.endswith('.txt'):
                loader = TextLoader(temp_path)
            else:
                raise ValueError("Unsupported file type")

            documents = loader.load()

            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            text_chunks = text_splitter.split_documents(documents)
            
            return text_chunks

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            os.rmdir(temp_dir)

    def vector_store(self, chunks):
        # Load Existing FAISS Database 
        vector_db_path =self.traning_pipline.vector_database
        embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=os.getenv("GEMINI_API_KEY"),
                model="models/embedding-001"
        )

        if os.path.exists(vector_db_path):
            faiss_db = FAISS.load_local(vector_db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
            logging.info("FAISS database loaded successfully.")
        else:
            faiss_db = FAISS(embeddings)
            logging.info("New FAISS database created.")

        # New Chunks to FAISS
        temp_db=faiss_db.add_documents(chunks,embeddings)
        faiss_db.merge_from(temp_db)
        logging.info("New document added to FAISS database.")

        # Save Updated FAISS Database
        faiss_db.save_local(vector_db_path)
        logging.info("FAISS database updated and saved.")


        return faiss_db,vector_db_path
    def new_vectore_Db(self):
        try:
            # Getting data 
            file=self.file
            # Chunking data
            chunks=self.process_document(file=file)

            # store data in vectore db
            self.vector_store(chunks)

            print('new data store competed')
            logging.info('New data Store completed')
        except Exception as e:
            print(e)
