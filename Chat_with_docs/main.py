import fitz  
import ollama
import streamlit as st

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def preprocess_text(text, chunk_size=512):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    similarities = [(chunk, cosine_similarity(query_embedding, embedding)) for chunk, embedding in VECTOR_DB]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

def generate_response(query):
    retrieved_chunks = retrieve(query)
    instruction_prompt = f'''You are a helpful assistant.
    Use only the following pieces of context to answer the question. Don't make up any new information:
    { '\n'.join([f' - {chunk}' for chunk, _ in retrieved_chunks]) }
    '''
    
    stream = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system', 'content': instruction_prompt},
            {'role': 'user', 'content': query}
        ],
        stream=True
    )
    
    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    
    return response

st.title("ChatWithDocs")
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    chunks = preprocess_text(pdf_text)

    for chunk in chunks:
        add_chunk_to_database(chunk)

    input_query = st.text_input("Ask a question:")

    if input_query:
        response = generate_response(input_query)
        st.write("Reply:")
        st.write(response)
