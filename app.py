from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import google.generativeai as genai
import fitz

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF file
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Get the first page
        first_page = pdf_document.load_page(0)
        # Get the image from the first page
        pix = first_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit3 = st.button("Percentage match")

input_prompt1 = """
You are a seasoned Technical Human Resources Manager. Your task is to thoroughly review the provided resume against the given job description.
Please provide a comprehensive professional evaluation of the candidate’s profile, assessing their alignment with the role.
Highlight the candidate’s key skills, strengths, and areas for improvement in relation to the job requirements.
Ensure your feedback is detailed and well-structured, with clear sections for each aspect of the evaluation.
"""

input_prompt3 = """
You are a highly skilled ATS (Applicant Tracking System) analyzer with extensive knowledge in data science and ATS functionalities.
Your task is to evaluate the resume against the provided job description and determine the percentage match.
Start with a precise match percentage, followed by a detailed analysis highlighting any missing keywords.
Conclude with a well-formatted summary of your final thoughts, emphasizing the strengths and weaknesses of the applicant.
Make sure your response is rich in detail and well-organized, using appropriate formatting to enhance readability.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        with st.spinner("Please wait..."):
            response=get_gemini_response(input_prompt1,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        with st.spinner("Please wait..."):
            response=get_gemini_response(input_prompt3,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
    else:
        st.write("Please uplaod the resume")



   




