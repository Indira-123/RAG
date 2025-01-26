# ChatWithDocs

`ChatWithDocs` is a Streamlit-based application that allows users to interact with PDF documents using natural language queries. It uses embedding and language models to retrieve relevant information from the uploaded PDF and generate context-based responses.

## Features
- **PDF Text Extraction**: Extract text from uploaded PDF files.
- **Text Chunking**: Break large text into manageable chunks for processing.
- **Embedding-Based Search**: Use a vector database to store text embeddings for efficient query-based retrieval.
- **LLM-Powered Responses**: Retrieve and generate responses based on the content using a language model.
- **Interactive UI**: Simple and intuitive interface using Streamlit.

---

## How It Works

1. Upload a PDF file.
2. The application extracts and processes text from the PDF.
3. Text chunks are embedded using the specified embedding model and stored in a vector database.
4. A query is entered into the text box, and the app retrieves the most relevant chunks based on similarity.
5. The retrieved information is used to generate a response using a language model.

## Models Used

-Embedding Model: CompendiumLabs/bge-base-en-v1.5-gguf
(109M parameters)

-Language Model: Bartowski/Llama-3.2-1B-Instruct-GGUF
(1.24B parameters)

---

