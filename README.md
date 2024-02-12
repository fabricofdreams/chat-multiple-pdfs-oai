## Multiple PDF Chat

This project enables users to chat with multiple PDF documents using Streamlit. It utilizes various libraries for text processing and conversation handling.

### Features:
- **PDF Text Extraction**: Extracts text from uploaded PDF documents.
- **Text Chunking**: Splits the extracted text into small, manageable chunks.
- **Embeddings Creation**: Generates embeddings for each text chunk using OpenAI embeddings.
- **Conversational Chain**: Establishes a conversational chain for handling user queries based on the processed PDF content.

### How to Use:
1. **Upload PDFs**: Upload your PDF documents via the file uploader in the sidebar.
2. **Ask Questions**: Enter your questions about the uploaded documents in the text input box.
3. **Conversation**: Receive responses based on the content of the documents.

### Usage:
- The main functionality is encapsulated in the `main()` function.
- PDF text extraction, chunking, embeddings creation, and conversation chain establishment are handled through separate functions.
- The user interface is built using Streamlit, allowing for intuitive interaction with the application.

### Dependencies:
- Streamlit
- PyPDF2
- dotenv
- langchain
- langchain_openai
- FAISS

### How to Run:
1. Ensure all dependencies are installed (`pip install -r requirements.txt`).
2. Run the script (`streamlit run app.py`).
3. Access the application through the provided URL.

Feel free to explore and enhance the capabilities of this project!
