import streamlit as st 
import os
import google.generativeai as genai

st.set_page_config(page_title="Chat Application" , page_icon="🤖")

st.sidebar.title("Enter the Google Gemini API Key")
API_KEY=st.sidebar.text_input("Enter the Google Gemini API Key" , type="password")
os.environ['GOOGLE_API_KEY']=API_KEY
genai.configure(api_key=API_KEY)

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question , stream=True)
    return response

st.header("Polaris AI - A Chatbot made with Gemini Pro")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]


input=st.text_input("Input: " , key="input")

submit = st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    st.session_state['chat_history'].append(("You" , input))
    st.subheader("The response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot" , chunk.text))
st.subheader("Chat History")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
    
        
    