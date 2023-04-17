"""Python file to serve as the frontend"""
import os
import sys
import streamlit as st
from streamlit_chat import message
from urllib.parse import urlparse
from langchain import OpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from prompt import QUESTION_PROMPT, COMBINE_PROMPT

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

st.set_page_config(page_title="Webpage QA Bot", page_icon=":robot:")
st.header("Webpage QA Bot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def get_api_key():
    api_key = st.text_input("Enter your OpenAI API key: ", key="apikey")
    return api_key

def get_urls():
    urls = st.text_input("Enter your url: ", key="url", on_change=lambda: st.session_state.input="").split(',')
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

@st.cache_data
def get_db(urls):
    loader = UnstructuredURLLoader(urls=urls)
    if len(loader.load()) == 0:
        st.error('Error when fetching url.')
        sys.exit(1)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    # Split your docs into texts
    texts = text_splitter.split_documents(loader.load())
    # Get embedding engine ready
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Embedd your texts
    db = FAISS.from_documents(texts, embeddings)
    return db

if input_ok and len(api_key) != 0 and len(query) != 0:
    db = get_db(urls)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0.7), retriever=db.as_retriever(), question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)

    if query:
        result = chain({"question": query})
        output = result['answer'].strip()

        st.session_state.past.append(query)
        st.session_state.generated.append(output)
        
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
