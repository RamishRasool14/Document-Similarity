import time

import streamlit as st

from utils import embedding, calculate_similarity, read_docx, read_pdf

from weaviate_client import WeaviateClient

weaviate_instance = WeaviateClient()

def main():
    st.title("Document Similarity Checker")

    uploaded_files = st.file_uploader("Choose two documents to compare", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files and len(uploaded_files) == 2 and all([file.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"] for file in uploaded_files]):
        st.success("Documents uploaded successfully!")

        text = []
        for file in uploaded_files:
            if file.type == "application/pdf":
                text.append(read_pdf(file))
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text.append(read_docx(file))

        button = st.button("Compare Documents", key='compare')

        if button:
            body, status = embedding(text)
            if status == 503:
                st.warning(f"{body.get('error')}. Please try again in {int(body.get('estimated_time'))} seconds.")
            elif status == 200:
                for i in range(2):
                    status = weaviate_instance.add_vector_to_weaviate(text[i], body[i])
                    if status:
                        st.success("Embedding successful and added to Weaviate!")
                    else:
                        st.error("Unable to add to Weaviate. Please check connection.")
                st.success(f"Embedding successful!\nSimilarity score: {calculate_similarity(body)}")
            elif status == 400:
                st.error(f"Hugging Face API Error: {body.get('error')}")

        st.subheader("Document 1:")
        st.text_area("Text Content", text[1], key='doc1')

        st.subheader("Document 2:")
        st.text_area("Text Content", text[0], key='doc2')

    else:
        st.warning("Please upload exactly two documents of type PDF or DOCX")

if __name__ == "__main__":
    main()
