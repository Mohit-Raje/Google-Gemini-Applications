from dotenv import load_dotenv
import streamlit as st 
import os
import google.generativeai as genai

load_dotenv()
os.environ['GOOGLE_API_KEY']="Enter API Key here"

genai.configure(api_key="Enter API Key here")


##Function To load Gemini Pro model
model=genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")

def get_gemini_response(question):
    response=model.generate_content(question)
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")


input=st.text_input("Input : " , key="input")
submit=st.button("Ask the question")


if submit:
    response = get_gemini_response(input)
    st.subheader("Response : ")
    st.write(response.text)
    
    
