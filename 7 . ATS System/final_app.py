import streamlit as st 
import os
from PIL import Image 
import pdf2image
import google.generativeai as genai
import io
import base64
import PyPDF2  as pdf

## Setup streamlit page
st.set_page_config(page_title="AI Resume Match Assistant" , page_icon="🔍")
st.header("AI Resume Match Assistant - A ATS System")

st.sidebar.title("Enter the Google API Key")
api_key=st.sidebar.text_input(label="Enter the API Key" , type="password")

genai.configure(api_key=api_key)
os.environ["GOOGLE_API_KEY"]=api_key


def get_gemini_response(input , pdf_content , prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input , pdf_content[0] , prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        reader=pdf.PdfReader(uploaded_file)
        text=""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text+=str(page.extract_text())
        return text
        
    else:
        raise FileNotFoundError("No file uploaded")



input_text=st.text_area("Job Description (JD): ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Provide the percentage match and suggestions with respect to JD")

# submit3 = st.button("Percentage match - Malfunctioning")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

Give the percentage match and all the imporvements need in summarized format and help 
the candidate secure job .

Give the output in form : JD Match":"%","MissingKeywords:[]" and imporvements in summarized format 
do not print the jd and resume.
also give the impoved version of the provided resume that matches the jd more than 80%

"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    pdf_content = input_pdf_setup(uploaded_file)
    input_prompt2 = input_prompt2.format(text=pdf_content, jd=input_text)
    response=get_gemini_response(input_prompt2 , pdf_content , input_text )
    st.write(response)
    
# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         # st.write(pdf_content)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")
