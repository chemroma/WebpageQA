"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import pickle
from urllib.parse import urlparse

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

def get_urls():
    urls = st.text_input("Enter your url: ", key="url")
    return urls


def get_text():
    input_text = st.text_input("Enter your OpenAI API key: ", key="input")
    return input_text

urls = get_urls()
user_input = get_text()

placeholder = st.empty()
input_ok = True
for url in urls:
    if not uri_validator(url):
        input_ok = False

if not input_ok:
    placeholder.error('please input a valid url.')

if input_ok:
    st.info('url is ok')
    placeholder.empty()
    if user_input:
        # result = chain({"question": user_input})
        output = user_input

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    # message(user_input, is_user=True)  # align's the message to the right
    # message(user_input)
        
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
