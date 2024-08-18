import streamlit as st
import arxiv
import google.generativeai as genai
import requests
from io import BytesIO

def get_pdf_content(arxiv_url):
    try:
        # Extract the arXiv ID from the URL
        arxiv_id = arxiv_url.split('/')[-1]
        
        # Search for the paper using the arxiv ID
        search = arxiv.Search(id_list=[arxiv_id])
        result = next(search.results(), None)
        
        if result:
            pdf_url = result.pdf_url
            response = requests.get(pdf_url)
            if response.status_code == 200:
                pdf_content = BytesIO(response.content)
                return pdf_content, pdf_url
            else:
                st.error("Failed to download PDF.")
                return None, None
        else:
            return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# def summarize_pdf(model, pdf) -> str:
    

# Sidebar for API key input
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your API key", type="password")
st.sidebar.write("If you don't have API Key, get one free here: https://aistudio.google.com/app/apikey")
if not api_key:
    st.sidebar.warning("Please enter an API key to proceed.")
if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        if response:
            st.sidebar.success("Your API Key is valid!")
    except:
        st.sidebar.error("Your API Key is not valid!")


# Streamlit App
st.title("arXiv PDF Access")

arxiv_url = st.text_input("Enter arXiv link:")

if st.button("Get PDF"):
    if arxiv_url:
        with st.spinner("Fetching PDF..."):
            pdf_content, pdf_url = get_pdf_content(arxiv_url)
            if pdf_content:
                st.success("PDF downloaded successfully!")
                st.write(f"[Download PDF directly]({pdf_url})")
                st.download_button(
                    label="Download PDF",
                    data=pdf_content,
                    file_name=f"{arxiv_url.split('/')[-1]}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to retrieve PDF. Please check the URL.")
    else:
        st.write("Please enter a valid arXiv URL.")
