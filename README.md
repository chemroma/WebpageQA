# Webpage QA Bot
Build with [langchain](https://github.com/hwchase17/langchain) and [Streamlit](https://streamlit.io/). Inspired by [hwchase17/notion-qa](https://github.com/hwchase17/notion-qa).

![pLCyK.png](https://s1.imgbed.xyz/2023/04/17/pLCyK.png)

# Brief Introduction
Enter a url, then ask!

## Overall process
Enter URL->Get web page content->Segment text->Vectorize text->Vectorize user question->Calculate similarity between user question and web page content->Extract text related to the question from the web page->Add the question and related text to the Prompt->Submit to LLM to get answer.

## Prerequisite
- An openai api key
- A webpage url
- A question

You can try online demo [here](https://chemroma-webpageqa-app-teafso.streamlit.app/).

