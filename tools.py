import re
from typing import Any, List, Tuple, Union

from bs4 import BeautifulSoup
from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import Tool, tool
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.utilities import (BashProcess, GoogleSearchAPIWrapper,
                                 TextRequestsWrapper)
from langchain.vectorstores import FAISS

from customTools.ChromaQA import CustomQASystem
from customTools.ExtractContent import ExtractTextContentFromUrl
from customTools.ListFilesTools import ListFilesInADirectory
from customTools.terraform import TerraformValidateTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

search = GoogleSearchAPIWrapper(k=1)
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

listfilestool = ListFilesInADirectory()
extractContent = ExtractTextContentFromUrl()

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
     Tool(
        name=listfilestool.name,
        func=listfilestool.run,
        description=listfilestool.description
    ),
    Tool(
        name="Ask Padok repositories",
        func=CustomQASystem("/Users/stan/Dev/Padok/vercel-langchain/chroma/stangirard/terraform").run,
        description="useful for when you want to ask about   terraform, yatas, Terraform guides, guidelines, modules, aws, azure, gcp, golang, kubernetes"
    ),

     Tool(
        name=extractContent.name,
        func=extractContent.run,
        description=extractContent.description,
    ),
    Tool(
        name="Run a bash command",
        func=BashProcess().run,
        description="useful for when you want to run a bash command"
    ),
    TerraformValidateTool(),
    WriteFileTool(),
    ReadFileTool(),

]

docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(tools)]
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = vector_store.as_retriever()

def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [tools[d.metadata["index"]] for d in docs]