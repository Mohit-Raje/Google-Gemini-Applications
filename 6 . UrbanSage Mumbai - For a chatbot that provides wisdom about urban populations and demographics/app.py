import os
import streamlit as st 
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai 
from langchain.chains import create_retrieval_chain
import time
import PyPDF2


st.set_page_config(page_title = "UrbanSage" , page_icon="🌍")

st.sidebar.title("Enter the API Keys")
groq_api_key=st.sidebar.text_input("Enter Groq API Key")
os.environ['GROQ_API_KEY']=groq_api_key

google_api_key=st.sidebar.text_input("Enter Google Gemini API Key")
os.environ['GOOGLE_API_KEY']=google_api_key

st.sidebar.write("For downloading the document click the button below")
pdf_path = "census/mumbai population.pdf"
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    pdf_content = ""
    for page in reader.pages:
        pdf_content += page.extract_text()
    
st.sidebar.download_button(
    label="Download PDF",
    data=pdf_content,
    file_name="mumbai-population.pdf",
    mime="application/pdf"
)

genai.configure(api_key=google_api_key)

st.title("UrbanSage Mumbai - For a chatbot that provides wisdom about urban populations and demographics.")


llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="gemma2-9b-it")

prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

def vector_embedding():

    if "vectors" not in st.session_state:

        st.session_state.embeddings=GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        st.session_state.loader=PyPDFDirectoryLoader("census") ## Data Ingestion
        st.session_state.docs=st.session_state.loader.load() ## Document Loading
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200) ## Chunk Creation
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:20]) #splitting
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings) #vector OpenAI embeddings




if st.button("Document Embedding"):
    vector_embedding()
    st.write("Vector Store DB Is Ready")


prompt1=st.text_input("Enter Your Question Census Document")

import time



if prompt1:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    start=time.process_time()
    response=retrieval_chain.invoke({'input':prompt1})
    st.write("Response time :",time.process_time()-start)
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")


st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: black;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            z-index: 100;
        }
        .footer a {
            color: white;
            text-decoration: none;
        }
        .footer img {
            width: 30px;
            vertical-align: middle;
            margin-left: 10px;
        }
    </style>
    <div class="footer">
        <strong>CopyRight © 2025 Mohit Raje</strong>
        <a href="https://github.com/Mohit-Raje" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
    
