import os
from operator import itemgetter
from typing import Dict, List, Optional, Sequence, Tuple

# import weaviate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatCohere
from langchain_community.vectorstores import Weaviate
from langchain_core.documents import Document
from langchain_core.language_models import LanguageModelLike
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import (
    ConfigurableField,
    Runnable,
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
    chain,
)

# from ingest import get_retriever, get_intent_retriever

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_fireworks import ChatFireworks
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langsmith import Client

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

import re
import string
import json

import requests
from dotenv import load_dotenv

load_dotenv()


# from search_fqa import searchSimilarity, encode
import pandas as pd

embed_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "./Chatbot_30102024",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True,
)
num_documents = len(vectorstore.index_to_docstore_id)
print(f"Total number of documents: {num_documents}")
retrieve = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.6, "fetch_k": num_documents, "k": num_documents},
)

@chain
def retriever(query: str) -> List[Document]:
    docs, scores = zip(*vectorstore.similarity_search_with_relevance_scores(query, score_threshold=0.6, k=num_documents))
    for doc, score in zip(docs, scores):
        doc.metadata["score"] = float(score)
    return docs

question = "Security in storage"
search_id = "27040"
docs1 = retriever.invoke(question)[0]
for doc in docs1:
    print(doc)