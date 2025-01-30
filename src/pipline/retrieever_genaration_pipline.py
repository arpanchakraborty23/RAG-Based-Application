from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from src.config.config import TraningPiplineConfig
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from src.logging import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()

class RetrieverGenaration:
    def __init__(self):
        self.traning_pipline_config=TraningPiplineConfig()

        logging.info("Retrieval Process Started")
        # Load embedding
        embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=os.getenv("GEMINI_API_KEY"),
                model="models/embedding-001"
        )
        # Load FAISS Vector Store
        vector_db_path = self.traning_pipline_config.vector_database
        print(vector_db_path)

        if os.path.exists(vector_db_path):
            self.faiss_db = FAISS.load_local(vector_db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
            print("FAISS index loaded successfully.")
        logging.info("FAISS database loaded")
        
        ## LLm
        self.llm=GoogleGenerativeAI(
            api_key=os.getenv('GEMINI_API_KEY'),
            model='gemini-pro',
            top_k=3
        )

        ## add memory
        self.memory= ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        logging.info('LLm Model Loaded')

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.faiss_db.as_retriever(),
            memory=self.memory
            )
        

    def get_response(self,query):
        try:
            response=self.qa({"question":query})
            print(response)
            logging.info('Data Genaration completed')
            print('Data Genaration completed')

            return response['answer']

        except Exception as e:
            logging.info(f"Error in retrieval: {str(e)}")
            raise e
        
if __name__=="__main__":
    obj=RetrieverGenaration(query='what is foundation model')
    print('*'*45)
    print()
    print(obj.get_response())