import streamlit as st
import arxiv

def search_arxiv(query, max_results=10):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    results = []
    for result in search.results():
        results.append({
            'title': result.title,
            'summary': result.summary,
            'link': result.entry_id,
            'authors': [author.name for author in result.authors],
            'published': result.published
        })
    
    return results

# Streamlit App
st.title("arXiv Article Search")

query = st.text_input("Enter search keyword:")
max_results = st.slider("Number of results", 1, 50, 10)

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            articles = search_arxiv(query, max_results)
            if articles:
                for article in articles:
                    st.subheader(article['title'])
                    st.write(f"**Authors**: {', '.join(article['authors'])}")
                    st.write(f"**Published on**: {article['published'].strftime('%Y-%m-%d')}")
                    st.write(article['summary'])
                    st.write(f"[Read more]({article['link']})")
                    st.write("---")
            else:
                st.write("No results found.")
    else:
        st.write("Please enter a search keyword.")
