"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import pickle
from urllib.parse import urlparse

from langchain.document_loaders import UnstructuredURLLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain

from prompt import QUESTION_PROMPT, COMBINE_PROMPT
import os

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

# From here down is all the StreamLit UI.
st.set_page_config(page_title="Blendle Notion QA Bot", page_icon=":robot:")
st.header("Blendle Notion QA Bot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def get_api_key():
    api_key = st.text_input("Enter your OpenAI API key: ", key="apikey")
    return api_key

def get_urls():
    urls = st.text_input("Enter your url: ", key="url").split(',')
    return urls

def get_query():
    input_text = st.text_input("Enter your question: ", key="input")
    return input_text

api_key = get_api_key()
urls = get_urls()
query = get_query()

os.environ['OPENAI_API_KEY'] = api_key

input_ok = True
for url in urls:
    if len(url) !=0 and not uri_validator(url.strip()):
        input_ok = False

if not input_ok:
    st.error('please input a valid url.')

if input_ok and len(api_key) != 0 and len(query) != 0:
    st.info(urls)
    st.info(query)
    loader = UnstructuredURLLoader(urls=urls)
    st.info(len(loader.load()))
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    # Split your docs into texts
    texts = text_splitter.split_documents(loader.load())
    # Get embedding engine ready
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Embedd your texts
    db = FAISS.from_documents(texts, embeddings)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0.7), retriever=db.as_retriever(), question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)

    if query:
        result = chain({"question": query})
        output = result['answer'].strip()

        st.session_state.past.append(query)
        st.session_state.generated.append(output)

    # message(query, is_user=True)  # align's the message to the right
    # message(query)
        
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
