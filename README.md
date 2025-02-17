# RAG-Based-Application
This project implements RAG-Based-Application with Flask, FAISS Vector Database, MySQL, and AWS S3 for handling file uploads, processing documents, storing chat history, and generating responses using Retriever-Augmented Generation (RAG).
## Workflows

1. **Data Ingestion**
    - Documents  ingested from web sources using WebBaseLoader
    - Load documents from URLs and process them similarly


2. **Document Upload and Processing**
    - User uploads documents to the system through the Artifacts
    - Files are stored in AWS S3
    - Documents are processed and converted to text
    - Text is split into chunks for embedding

3. **Vector Database Creation**
    - Text chunks are embedded using Google Embeddings
    - Embeddings are stored in FAISS vector database

4. **Query Processing**
    - User sends a query through the chat interface
    - Query is embedded using the same embedding model
    - Similar chunks are retrieved from FAISS


5. **Response Generation**
    - Retrieved chunks are used as context
    - Response is generated using RAG
    - Chat history is stored in MySQL
    - Response is returned to user
## Knowledge Base

1. **Document Loading**
    ```python
    from langchain.document_loaders import WebBaseLoader
    
    # Load document from URL
    loader = WebBaseLoader("")
    documents = loader.load()
    ```

2. **Text Chunking**
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    ```

3. **FAISS Database Creation**
    ```python
    from langchain.embeddings import GoogleEmbeddings
    from langchain.vectorstores import FAISS
    
    # Create embeddings and store in FAISS
    embeddings = GoogleEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    ```
## Tools and Technologies
## Data Pipeline

1. **Data Ingestion**
    ```python
    from langchain.document_loaders import 
    WebBaseLoader

    from langchain.document_loaders import WebBaseLoader

    # Load documents from web sources
    loader = WebBaseLoader(url)
    documents = loader.load()
    ```
  

2. **Data Preprocessing**
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Create text chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents(clean_documents)
        return chunks

    ```

3. **Vector Database Pipeline**
    ```python
    from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
    from langchain.vectorstores import FAISS
    
    # Create embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    # save 
    vectorstore.save_local("index")
    ```
## Tools

- **Python**: Primary programming language
- **Flask**: Web framework for building the API endpoints
- **FAISS**: Vector database for efficient similarity search
- **MySQL**: Database for storing chat history and file metadata
- **AWS S3**: Cloud storage for document uploads
- **Langchain**: Framework for developing RAG applications
- **Google Embeddings**: For accessing language models and embeddings
- **Docker**: Containerization platform for packaging the application
- **Docker Compose**: Tool for defining and running multi-container Docker applications

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RAG-Based-Application.git
cd RAG-Based-Application
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file with:
```
LLM_API_KEY=""
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_BUCKET_NAME=""
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Testing with Postman

1. Import the Postman collection from `postman/RAG-Based-Application.json`

2. Available endpoints:
    - POST `/upload` - Upload documents
    - POST `/chat` - Send messages and get responses
    - GET `/history` - Retrieve chat history

3. Test the endpoints:
    - Use the pre-configured requests in the Postman collection
    - Ensure proper authentication headers are set
    - Check response status codes and data format
