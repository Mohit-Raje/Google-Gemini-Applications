import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set the page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Gemini Image Demo")


# Sidebar for API key input
st.sidebar.title("API Key Input")
API_KEY = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Set the API key as an environment variable
os.environ['GOOGLE_API_KEY'] = API_KEY

# Configure the Generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the response function
def response(input, img):
    if input != "":
        result = model.generate_content([input, img])
    else:
        result = model.generate_content(img)
    return result.text

# Main application content
st.header("Gemini Image Application")
input_text = st.text_input("Input Prompt:", key="input")

uploaded_image = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
image = ""
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

submit = st.button("Tell me about Image")

if submit:
    if API_KEY:
        try:
            result = response(input_text, image)
            st.subheader("The Response is:")
            st.write(result)
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.error("Please enter a valid API Key in the sidebar.")
