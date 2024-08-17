import streamlit as st
import arxiv

def get_pdf_link(arxiv_url):
    try:
        # Extract the arXiv ID from the URL
        arxiv_id = arxiv_url.split('/')[-1]
        
        # Search for the paper using the arxiv ID
        search = arxiv.Search(id_list=[arxiv_id])
        result = next(search.results(), None)
        
        if result:
            return result.pdf_url
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit App
st.title("arXiv PDF Access")

arxiv_url = st.text_input("Enter arXiv link:")

if st.button("Get PDF"):
    if arxiv_url:
        with st.spinner("Fetching PDF link..."):
            pdf_link = get_pdf_link(arxiv_url)
            if pdf_link:
                st.success("PDF link found!")
                st.write(f"[Download PDF]({pdf_link})")
            else:
                st.error("Failed to find PDF link. Please check the URL.")
    else:
        st.write("Please enter a valid arXiv URL.")
