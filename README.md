# Webpage QA Bot
Build with [LangChain](https://github.com/hwchase17/langchain) and [Streamlit](https://streamlit.io/). Inspired by [hwchase17/notion-qa](https://github.com/hwchase17/notion-qa).

![pLCyK.png](https://s1.imgbed.xyz/2023/04/17/pLCyK.png)

# Brief Introduction
Enter url, then ask! 

## Overall process
Enter URL->Get web page content->Segment text->Vectorize text->Vectorize user question->Calculate similarity between user question and web page content->Extract text related to the question from the web page->Add the question and related text to the Prompt->Submit to LLM to get answer.

[![pLdqh.md.png](https://s1.imgbed.xyz/2023/04/17/pLdqh.md.png)](https://www.imgbed.com/image/pLdqh)

The overall process is shown in the above diagram, where the Local Documents refers to the web page content in this project.

## Prerequisite
- An openai api key (if you don't have ,click [here](https://platform.openai.com/account/api-keys) to get one)
- A webpage url
- A question

You can try online demo [here](https://chemroma-webpageqa-app-teafso.streamlit.app/).

# Todo
- [ ] Optimizing code
- [ ] Fix the problem of failure to retrieve certain web page content
