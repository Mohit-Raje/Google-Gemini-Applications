import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai


st.set_page_config(page_title="Multi Language Invoice extractor" , page_icon="🧙‍♂️")
st.header("MultiLang Invoice Wizard")
st.sidebar.title("Enter Google Gemini API Key : ")
API_KEY=st.sidebar.text_input("Enter API Key" , type="password")

google_api_key=API_KEY
genai.configure(api_key=API_KEY)
os.environ['GOOGLE_API_KEY']=API_KEY

model=genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(prompt , img , input):
    response=model.generate_content([input , img[0] , prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        
        bytes_data=uploaded_file.getvalue()
        images_parts=[{
            'mime_type' : uploaded_file.type,
            "data":bytes_data
        }]

        return images_parts
    else:
        raise FileNotFoundError("File not found")
    

input=st.text_input("Input prompt: " , key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...." , type=['jpg' , 'jpeg' , 'png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image , caption="Uploaded Iamge")
    
submit=st.button("Tell me about the image")
input_prompt="""
You are an expert in understanding invoices . We will upload a image as invoice 
and you will have to any questions based on the uploaded invoice image
"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt , image_data , input)
    st.subheader("Response is : ")
    st.write(response)
