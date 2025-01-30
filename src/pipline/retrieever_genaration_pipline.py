from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from src.config.config import TraningPiplineConfig
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA
from src.logging import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()

class RetrieverGenaration:
    def __init__(self,query):
        self.query=query
        self.traning_pipline_config=TraningPiplineConfig()

        logging.info("Retrieval Process Started")

    def get_relevant_documents(self):
        try:
            # Load FAISS Vector Store
            embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=os.getenv("GEMINI_API_KEY"),
                model="models/embedding-001"
            )

            vector_db_path = self.traning_pipline_config.vector_database
            print(vector_db_path)

            if os.path.exists(vector_db_path):
                faiss_db = FAISS.load_local(vector_db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
                print("FAISS index loaded successfully.")
            logging.info("FAISS database loaded")
            ## LLm
            llm=GoogleGenerativeAI(
            api_key=os.getenv('GEMINI_API_KEY'),
            model='gemini-pro',
            top_k=3
            )
            logging.info('LLm Model Loaded')
            qa= RetrievalQA.from_chain_type(
                llm=llm,
                chain_type='stuff',
                retriever=faiss_db.as_retriever()
            )
            response=qa.invoke(self.query)
            print(response)
            logging.info('Data Genaration completed')
            print('Data Genaration completed')

            return response

        except Exception as e:
            logging.error(f"Error in retrieval: {str(e)}")
            raise e
if __name__=="__main__":
    obj=RetrieverGenaration(query='what is deepseek llm')
    print(obj.get_relevant_documents())