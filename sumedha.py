import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

genai.configure(api_key="AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def query_with_cag(context: str, query: str) -> str:
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

st.title("Suemdha RAG Application Chatbot")
st.header("Upload a PDF and Ask Your Query......")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
    st.session_state.pdf_text = None

uploaded_file = st.file_uploader("Please upload a PDF file", type="pdf")

if uploaded_file is not None:
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    pdf_text = read_pdf(temp_file_path)
    st.session_state.uploaded_file = uploaded_file
    st.session_state.pdf_text = pdf_text

    st.text_area("PDF Content Preview", value=pdf_text[:1000], height=150)

    continue_or_upload = st.radio("Do you want to continue or upload a new file?", 
                                 ("Continue", "Upload New File"))

    if continue_or_upload == "Upload New File":
        st.session_state.uploaded_file = None
        st.session_state.pdf_text = None
        st.experimental_rerun()  

    if st.session_state.uploaded_file is not None:
        query = st.text_input("Ask a question based on the content of the PDF:")

        if query:
            response = query_with_cag(st.session_state.pdf_text, query)
            st.write("Answer:", response)
