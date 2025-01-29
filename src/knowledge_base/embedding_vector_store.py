import os
import json
from src.logging import logging
from src.config.config import TraningPiplineConfig
from src.config.artifacts_entity import DataChunkingArtifacts,VectorDataBaseArtifacts
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

class VectorDatabase:
    def __init__(self,data_chunking_artifacts:DataChunkingArtifacts):
        self.data_chunking_artifact=data_chunking_artifacts
        self.traning_pipline_config=TraningPiplineConfig()
        print('Storing data in vector db started')

    def load_json(self,filename):
        with open(filename,'r',encoding='utf-8') as f:
            chunks=json.load(f)
        return chunks
    
    def store_data_in_vectordb(self,chunks):
        logging.info('storing data in vecore db')
        
        # load embedding model
        embeddings=GoogleGenerativeAIEmbeddings(
            google_api_key=os.getenv('GEMINI_API_KEY'),
            model="models/embedding-001"
        )

        # store data in vectore db
        vector_db=FAISS.from_texts(
            chunks,
            embeddings
        )

        logging.info(f' Total no of index: {vector_db.index.ntotal}')

        return vector_db
    
    def initate_vector_store(self):
        try:
            logging.info('vectore store started')

            # data path
            data_path=self.data_chunking_artifact.chunking_data_path
            print(data_path)

            # load data
            chunks=self.load_json(data_path)
            logging.info('data loaded')

            db=self.store_data_in_vectordb(chunks=chunks)

            # database path
            database_path=self.traning_pipline_config.vector_database
            db.save_local(folder_path=database_path)

            logging.info(f'vectore data base store path :{database_path}')

            print('Store data vectore database completed')
            return VectorDataBaseArtifacts(vector_database_path=database_path)


        except Exception as e:
            print(e)