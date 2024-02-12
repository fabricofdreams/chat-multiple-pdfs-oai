import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import *


def get_pdf_text(pdf_docs):
    """
    Get the text from a PDF
    """
    text = ''
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    """
    Split the text into small chunks
    """
    text_splitter = CharacterTextSplitter(
        separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks


def get_vectorstore(text_chunks):
    """
    Create embeddings for each chunk
    """
    embeddings = OpenAIEmbeddings()
    vectorestore = FAISS.from_texts(text_chunks, embeddings)
    return vectorestore


def get_conversation_chain(vectorstore):
    """
    Get the conversation chain
    """
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain


def handle_user_question(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(response['chat_history']):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

    pass


def main():
    load_dotenv()
    st.set_page_config(page_title='Multiple PDF Chat',
                       page_icon='🦄', layout='wide')

    st.write(css, unsafe_allow_html=True)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat with multiple PDFs 🦄')
    user_question = st.text_input('Ask a question about your documents:')

    if user_question:
        handle_user_question(user_question)

    with st.sidebar:
        st.subheader('Your documents:')
        pdf_docs = st.file_uploader(
            'Upload your PDFs here and click on Process', accept_multiple_files=True)
        if st.button('Process'):
            with st.spinner('Processing...'):
                # Get the PDFs content
                raw_text = get_pdf_text(pdf_docs)

                # Split content into small chunks
                text_chunks = get_text_chunks(raw_text)

                # Create embeddings for each chunk
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
