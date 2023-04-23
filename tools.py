from typing import Any, List, Tuple, Union
from bs4 import BeautifulSoup
from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import Tool, tool
from langchain.utilities import GoogleSearchAPIWrapper, TextRequestsWrapper
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import re

search = GoogleSearchAPIWrapper()
request = TextRequestsWrapper()
llm = OpenAI(temperature=0)


def extract_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    text = text[:1000]
    return text

def extract_texts_from_urls(url_list: List[str]) -> dict[str, str]:
    url_to_text_map = {}
    for url in url_list:
        html_content = request.get(url)
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()
        text = text[:200]
        url_to_text_map[url] = text
    return url_to_text_map

def ask_open_ai(question):
    template = "You are a helpful assistant that does exactly what is asked of you. You HAVE to be CONCISE. Here is the question"
    return llm(template + question)

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Lookup Content URL",
        func=request.get,
        description="useful for when you want to get the content of a webpage with a given url"
    ),
    Tool(
        name="HTML Text Extractor",
        func=extract_text,
        description="useful for when you want to extract only the text from an HTML page given one url"
    ),
    Tool(
        name="HTML Text Extractor for Multiple URLs",
        func=extract_texts_from_urls,
        description="useful for when you want to extract only the text from multiple HTML pages given a list of urls"
    ),
    Tool(
        name="Anything else you want",
        func=ask_open_ai,
        description="useful for when you want to ask open ai anything, or don't know what to do, or are stuck"
    )
]

docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(tools)]
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = vector_store.as_retriever()

def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [tools[d.metadata["index"]] for d in docs]