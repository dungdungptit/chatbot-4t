# Import libraries
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

# from search_fqa import searchSimilarity, encode
import pandas as pd

# import torch


dict_replace = {
    "2k|2k|2k|2k|2k": "200",
    "a": "anh",
    "ac": "anh chị",
    "a/c": "anh chị",
    "add|ad|adm|addd": "admin",
    "ak|ah": "à",
    "b": "bạn",
    "baoh|bh": "bao giờ",
    "bhyt": "bảo hiểm y tế",
    "bn|bnh|baonh": "bao nhiêu",
    "bâyh": "bây giờ",
    "cccd": "căn cước công dân",
    "chòa": "chào",
    "cj": "chị",
    "ck": "chuyển khoản",
    "chỉ tiêu": "chỉ tiêu tuyển sinh",
    "chỉ tiêu tuyển sinh tuyển sinh": "chỉ tiêu tuyển sinh",
    "clc": "chất lượng cao",
    "cmnd": "chứng minh nhân dân",
    "dgnl": "đánh giá năng lực",
    "dgtd": "đánh giá tư duy",
    "dhqg": "đại học quốc gia",
    "dkxt": "đăng ký xét tuyển",
    "dko": "được không",
    "đko": "được không",
    "dky|dki|đăng kí|dki|đki": "đăng ký",
    "đkxt|dkxt": "đăng ký xét tuyển",
    "hvcnbtvt": "Học viện Công nghệ Bưu chính Viễn thông",
    "d|đ": "điểm",
    "e": "em",
    "gddt|gd dt|gdđt|gd đt": "giáo dục đào tạo",
    "gd": "giáo dục",
    "hc": "học",
    "hcm": "hồ chí minh",
    "hnay": "hôm nay",
    "hqua": "hôm qua",
    "điểm tuyển sinh": "điểm trúng tuyển",
    "điểm đỗ": "điểm trúng tuyển",
    "điểm chuẩn|điểm": "điểm trúng tuyển",
    "điểm trúng tuyển đỗ": "điểm trúng tuyển",
    "điểm trúng tuyển điểm trúng tuyển": "điểm trúng tuyển",
    "điểm trúng tuyển trúng tuyển": "điểm trúng tuyển",
    "điểm trúng tuyển tuyển sinh": "điểm trúng tuyển",
    "điểm trúng tuyển": "điểm trúng tuyển",
    "điểm trúng tuyển nổi bật": "điểm nổi bật",
    "điểm trúng tuyển ưu tiên": "điểm ưu tiên",
    "điểm trúng tuyển cộng": "điểm cộng",
    "cộng điểm trúng tuyển": "cộng điểm",
    "điểm trúng tuyển thưởng": "điểm thưởng",
    "hv": "học viện",
    "j": "gì",
    "ko|k|kh|khg|kg|hong|hok|khum": "không",
    "ktx": "ký túc xá",
    "kt": "Kế toán",
    "kv|khvuc|kvuc": "khu vực",
    "lm": "làm",
    "lpxt": "lệ phí xét tuyển",
    "m": "mình",
    "mn": "mọi người",
    "tkdh": "thiết kế đồ họa",
    "mk": "mình",
    "nnao": "như nào",
    "ntn": "như thế nào",
    "nv|nvong": "nguyện vọng",
    "oke|oki|okeee": "ok",
    "p": "phải",
    "pk": "phải không",
    "q1|q9": "quận",
    "r": "rồi",
    "sdt|sđt|dt|đt": "số điện thoại",
    "sv": "sinh viên",
    "t": "tôi",
    "thpt": "trung học phổ thông",
    "thptqg": "trung học phổ thông quốc gia",
    "tk": "tài khoản",
    "tmdt": "Thương mại điện tử",
    "tnthpt": "trắc nghiệm trung học phổ thông",
    "tp hcm": "thành phố hồ chí minh",
    "trg|tr|trườg": "trường",
    "trường": "học viện",
    "ttnv": "thứ thự nguyện vọng",
    "tt": "thông tin",
    "uh|uk|um": "ừ",
    "vc": "việc",
    "vd": "ví dụ",
    "vs": "với",
    "z|v": "vậy",
    "đc|dc": "được",
    "năm nay": "2024",
    "năm ngoái|năm trước": "2023",
    "A1|a1": "A01",
    "A0|a0": "A00",
    "D1|d1": "D01",
    "A01": "tổ hợp xét tuyển A01",
    "A00": "tổ hợp xét tuyển A00",
    "D01": "tổ hợp xét tuyển D01",
    "hsg": "học sinh giỏi",
    "giải 1": "giải nhất học sinh giỏi",
    "giải nhất học sinh giỏi học sinh giỏi": "giải nhất học sinh giỏi",
    "giải 2": "giải nhì học sinh giỏi",
    "giải nhì học sinh giỏi học sinh giỏi": "giải nhì học sinh giỏi",
    "giải 3": "giải ba học sinh giỏi",
    "giải ba học sinh giỏi học sinh giỏi": "giải ba học sinh giỏi",
    "tổ hợp": "tổ hợp xét tuyển",
    "khối": "tổ hợp xét tuyển",
    "tổ hợp xét tuyển tổ hợp xét tuyển": "tổ hợp xét tuyển",
    "tổ hợp xét tuyển xét tuyển xét tuyển xét tuyển": "tổ hợp xét tuyển",
    "hsnl": "hồ sơ năng lực",
    "hthuc": "hình thức",
    "hthức": "hình thức",
    "hso": "hồ sơ",
    "hs": "hồ sơ",
    "nl": "năng lực",
    "hssv": "hồ sơ sinh viên",
    "xttn": "xét tuyển tài năng",
    "xtkh|xthk": "xét tuyển kết hợp",
    "xt": "xét tuyển",
    "xtkn": "xét tuyển kết hợp",
    "hba": "học bạ",
    "rv": "review",
    "review": "thông tin",
    "pthuc": "phương thức",
    "pt": "phương thức",
    "ielts": "IELTS",
    "toefl": "TOEFL",
    "toeic": "TOEIC",
    "sat": "SAT",
    "act": "ACT",
    "toefl itp": "TOEFL ITP",
    "toefl ibt": "TOEFL iBT",
    "xét": "xét tuyển",
    "xét tuyển tuyển": "xét tuyển",
    "Tổ hợp xét tuyển": "tổ hợp xét tuyển",
    "ktdtvt": "kỹ thuật điện tử viễn thông",
    "dtvt|dt vt|đtvt|đt vt": "điện tử viễn thông",
    "vt": "Viễn thông",
    "attt": "An toàn thông tin",
    "ttdpt|ttđpt": "Truyền thông đa phương tiện",
    "cn dpt|cndpt": "Công nghệ đa phương tiện",
    "udu": "Công nghệ thông tin định hướng ứng dụng",
    "cntt udu": "Công nghệ thông tin định hướng ứng dụng",
    "cntt ứng dụng": "Công nghệ thông tin định hướng ứng dụng",
    "công nghệ thông tin ứng dụng": "Công nghệ thông tin định hướng ứng dụng",
    "cntt": "Công nghệ thông tin",
    "dpt|đpt": "đa phương tiện",
    "khmt": "Khoa học máy tính",
    "ktdk|ktđk": "Kỹ thuật điều khiển",
    "ktdktdh": "Kỹ thuật điều khiển và tự động hóa",
    "iot": "Công nghệ Internet vạn vật (IoT)",
    "qtkd": "Quản trị kinh doanh",
    "ngành kt": "Ngành kế toán",
    "mmt": "Mạng máy tính",
    "bc": "Báo chí",
    "cntc": "Công nghệ tài chính (Fintech)",
    "marketting|makettting|mkt": "marketing",
}


def normalize_replace_abbreviation_text(text):
    # text = re.sub(
    #     r"[\.,\(\)]", " ", text
    # )  # thay thế các kí tự đặc biệt bằng khoảng trắng
    # text = re.sub("<.*?>", "", text).strip()
    # text = re.sub("(\s)+", r"\1", text)
    # chars = re.escape(string.punctuation)
    # text = re.sub(
    #     r"[" + chars + "]", " ", text
    # )  # thay thế các kí tự đặc biệt bằng khoảng trắng
    text = re.sub(r"\s+", " ", text)  # thay thế nhiều khoảng trắng bằng 1 khoảng trắng
    text = text.strip()  # xóa khoảng trắng ở đầu và cuối
    text = text.lower()  # chuyển về chữ thường
    """ 
    # "cntt" -> "công nghệ thông tin"
    text = re.sub(r'\bcntt\b', 'công nghệ thông tin', text)
    # "ntn" -> "như thế nào"
    text = re.sub(r'\bntn\b', 'như thế nào', text)
    # "ad, adm" -> "admin"
    text = re.sub(r'\b(ad|adm)\b', 'admin', text)
    text = re.sub(r'\b(gd dt|gddt)\b', 'giáo dục đào tạo', text) 
    # điểm chuẩn -> điểm trúng tuyển
    text = re.sub(r'\bđiểm chuẩn\b', 'điểm trúng tuyển', text)
    """

    for k, v in dict_replace.items():
        text = re.sub(r"\b" + "(" + k + ")" + r"\b", v, text)

    return text.lower()


df2 = pd.read_csv("./data/Phan Cap (phan_cap) 18102024.csv", encoding='ISO-8859-1', sep=",")

def standard_name(text):
    res = df2.loc[df2['name'].str.fullmatch(text, na=False)].to_json(orient='records')
    res = json.loads(res)

    if len(res):
        return {'name': res[0]['name'], 'description': res[0]['description']}
    else:
        return {'name': text, 'description': text}

def search_standard_name(text):
    res = df2.loc[df2['name'].str.fullmatch(text, na=False)].to_json(orient='records')
    res = json.loads(res)

    if len(res):
        return res[0]
    else:
        return {'display_name': text, 'name': text, 'description': text, 'parrent': None, 'children': []}

def paser_standard(res):
    print(res)
    res = res
    full_name = res["display_name"].split("->")
    full_name = [search_standard_name(i.strip()) for i in full_name]
    # [print(i) for i in full_name]
    if len(full_name) > 1:
        for i in range(len(full_name) - 1):
            full_name[i]["children"] = [full_name[i + 1]]

    return full_name[0]


def search_standard(docs):
    #  {
    #   "page_content": "Information technology — Artificial intelligence — Assessment of machine learning classification performance\n\nThis document specifies methodologies for measuring classification performance of machine learning models, systems and algorithms.",
    #   "metadata": {
    #     "source": "https://www.iso.org/standard/79799.html?browse=ics",
    #     "seq_num": 28441,
    #     "domain": null,
    #     "id": "ISO/IEC TS 4213:2022",
    #     "branch": "ISO -> 35 -> 35.020",
    #     "year_public": null,
    #     "status": "Còn hiệu lực",
    #     "name_en": "Information technology — Artificial intelligence — Assessment of machine learning classification performance",
    #     "name_vn": null
    #   },
    #   "type": "Document"
    # },
    for index in range(len(docs)):
        # print(docs[index].metadata["branch"])
        docs[index].metadata["tree"] = {}
        if docs[index].metadata["branch"] != "" and docs[index].metadata["branch"] != None:
            print(docs[index].metadata["branch"])
            res = df2.loc[
                df2["display_name"].str.contains(str(docs[index].metadata["branch"]), na=False)
            ].to_json(orient="records")
            res = json.loads(res)

            # print(res)
            tmp = {}
            if len(res) > 0:
                tmp = res[0]
            else:
                tmp = {
                    "display_name": str(docs[index].metadata["branch"])
                }
            print(tmp)
            # paser_standard(tmp)
            docs[index].metadata["tree"] = paser_standard(tmp)
    return docs


from getpass import getpass
import os

# from langchain.llms import PromptLayerOpenAI

# PROMPTLAYER_API_KEY = getpass()
# os.environ["PROMPTLAYER_API_KEY"] = PROMPTLAYER_API_KEY

# load openai api key from file .env
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langchain.prompts import ChatPromptTemplate

""" 
--
Nếu câu trả lời có link ảnh (type: image) hoặc link đường dẫn, hãy sử dụng dấu gạch chân (_) theo cú pháp [ảnh](url) để thể hiện link ảnh hoặc [đường dẫn](url) link đường dẫn.
--
 """

# Prompt
template = """Từ câu hỏi, thông tin tổ chức và văn bản sau đây, hãy trả lời câu hỏi dựa trên \nQuestion: {question}\nOrganization: {organization}\nContext: {context}\n
Đưa ra câu trả lời là các standarzation liên quan nhất đến thông tin câu hỏi và context
Cần phân tách câu trả lời và trình bày như 1 danh sách có tối thiểu 10-15 (n) standarzation theo số thứ tự như mẫu sau:
1. 
2. 
3. 
.....
n. 
---\nOutput:"""

prompt = ChatPromptTemplate.from_template(template)

# get index
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embed_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "./Chatbot_17102024",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 15,
        # "threshold": 0.5
    }
)

template_vietnamese_fusion = """Bạn là một tư vấn viên chuyên nghiệp và là người giải quyết vấn đề, được giao nhiệm vụ trả lời bất kỳ câu hỏi nào \
về các thông tin về các standarzation.
Bạn có thể tạo ra nhiều truy vấn tìm kiếm dựa trên một truy vấn đầu vào duy nhất. \n
Tạo ra nhiều truy vấn tìm kiếm liên quan đến: {question} \n
Lưu ý đầu ra trả về các truy vấn tiếng Anh nhé
Đầu ra (3 truy vấn tiếng Anh):"""

prompt_rag_fusion = ChatPromptTemplate.from_template(template_vietnamese_fusion)

generate_queries = (
    prompt_rag_fusion
    | ChatOpenAI(temperature=0)
    | StrOutputParser()
    | (lambda x: x.split("\n"))
)

translate_prompt_template = """Bạn là 1 người giỏi tiếng anh và các ngôn ngữ khác bao gồm cả tiếng Việt. Với đầu vào sau đây: \n{question}Nếu câu đầu vào là tiếng Việt, hãy dịch trả về là tiếng Anh.
Nếu câu đầu vào là tiếng Anh, hãy trả về là tiếng Anh.
Đầu ra (Tiếng Anh):"""

translate_prompt = ChatPromptTemplate.from_template(translate_prompt_template)

translate_query = translate_prompt | ChatOpenAI(temperature=0) | StrOutputParser()

from langchain.load import dumps, loads


def reciprocal_rank_fusion(results: list[list], k=60):
    """Reciprocal_rank_fusion that takes multiple lists of ranked documents
    and an optional parameter k used in the RRF formula"""

    # Initialize a dictionary to hold fused scores for each unique document
    fused_scores = {}

    # Iterate through each list of ranked documents
    for docs in results:
        # Iterate through each document in the list, with its rank (position in the list)
        # print(docs)
        for rank, doc in enumerate(docs):
            # print(rank, doc)
            # Convert the document to a string format to use as a key (assumes documents can be serialized to JSON)
            doc_str = dumps(doc)
            # If the document is not yet in the fused_scores dictionary, add it with an initial score of 0
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            # Retrieve the current score of the document, if any
            previous_score = fused_scores[doc_str]
            # Update the score of the document using the RRF formula: 1 / (rank + k).
            fused_scores[doc_str] += 1 / (rank + k)

    # Sort the documents based on their fused scores in descending order to get the final reranked results
    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # Return the reranked results as a list of tuples, each containing the document and its fused score
    return reranked_results


def remove_duplicate_words(text: str):
    text = text.split()
    text = " ".join(sorted(set(text), key=text.index))
    return text


def get_results(question: str):
    question = normalize_replace_abbreviation_text(question)
    # docs = retrieval_chain_rag_fusion.invoke({"question": question})
    question = translate(question=question)
    docs1 = retriever.get_relevant_documents(question)
    # docs.append(docs1)
    # docs = reciprocal_rank_fusion(docs)
    return docs1


def translate(question: str):
    question = normalize_replace_abbreviation_text(question)
    question = translate_query.invoke({"question": question})
    print("===============================", question)
    return question


retrieval_chain_rag_fusion = generate_queries | retriever.map()


class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]]
    organization: str


def _format_chat_history(chat_history: List[Dict[str, str]]) -> List:
    converted_chat_history = []
    for message in chat_history:
        if message.get("human") is not None:
            converted_chat_history.append(HumanMessage(content=message["human"]))
        if message.get("ai") is not None:
            converted_chat_history.append(AIMessage(content=message["ai"]))
    return converted_chat_history


_inputs = RunnableParallel(
    {
        "question": lambda x: x["question"],
        "organization": itemgetter("organization"),
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
        "context": RunnableLambda(itemgetter("question")) | get_results,
    }
).with_types(input_type=ChatRequest)

final_rag_chain = _inputs | prompt | llm | StrOutputParser()

vu = {
    "vu_buu_chinh": """Vụ Bưu chính là tổ chức thuộc Bộ Thông tin và Truyền thông, thực hiện chức năng tham mưu, giúp Bộ trưởng quản lý nhà nước về bưu chính.""",
    "vu_ke_hoach_tai_chinh": """Vụ Kế hoạch – Tài chính là tổ chức thuộc Bộ Thông tin và Truyền thông, có chức năng tham mưu giúp Bộ trưởng thực hiện chức năng quản lý, tổng hợp về công tác chiến lược, quy hoạch, kế hoạch phát triển ngành, lĩnh vực; kế hoạch đầu tư phát triển và dự toán thu, chi ngân sách nhà nước; các chương trình đầu tư công, định mức kinh tế kỹ thuật và các nhiệm vụ tài chính, kế hoạch, thống kê; quản lý đầu tư xây dựng cơ bản; quản lý kinh tế về dịch vụ công; quản lý kinh tế chuyên ngành trong phạm vi quản lý nhà nước của Bộ.""",
    "vu_hop_tac_quoc_te": """Vụ Hợp tác quốc tế là tổ chức thuộc Bộ Thông tin và Truyền thông, có chức năng tham mưu giúp Bộ trưởng thực hiện quản lý về quan hệ đối ngoại, hội nhập và hợp tác quốc tế trong các lĩnh vực thuộc phạm vi quản lý nhà nước của Bộ Thông tin và Truyền thông.""",
    "vu_khoa_hoc_cong_nghe": """Vụ Khoa học và Công nghệ là tổ chức trực thuộc Bộ Thông tin và Truyền thông, có chức năng tham mưu giúp Bộ trưởng thực hiện quản lý nhà nước về khoa học và công nghệ, tiêu chuẩn đo lường chất lượng và bảo vệ môi trường trong các ngành, lĩnh vực thuộc phạm vi quản lý của Bộ Thông tin và Truyền thông.""",
    "vu_kinh_te_va_xa_hoi_so": """Vụ Kinh tế số và Xã hội số là tổ chức thuộc Bộ Thông tin và Truyền thông, thực hiện chức năng tham mưu giúp Bộ trưởng về phát triển kinh tế số, xã hội số; quản lý nhà nước về giao dịch điện tử theo quy định của pháp luật.""",
    "vu_phap_che": """Vụ Pháp chế là tổ chức thuộc Bộ Thông tin và Truyền thông, có chức năng tham mưu giúp Bộ trưởng thực hiện quản lý nhà nước bằng pháp luật trong lĩnh vực thông tin và truyền thông và tổ chức thực hiện công tác pháp chế theo quy định của pháp luật.""",
}
vu_en = {
    "vu_buu_chinh": """The Postal Department is an organization under the Ministry of Information and Communications, performing the function of advising and assisting the Minister in state management of postal services.""",
    "vu_ke_hoach_tai_chinh": """The Department of Planning and Finance is an organization under the Ministry of Information and Communications, with the function of advising and assisting the Minister in performing management and synthesis functions on strategy, planning, Sector and field development plans; development investment plans and state budget revenue and expenditure estimates; public investment programs, economic and technical norms and financial tasks, plans and regulations statistics; capital construction investment management; economic management of public services; specialized economic management within the scope of state management of the Ministry.""",
    "vu_hop_tac_quoc_te": """The Department of International Cooperation is an organization under the Ministry of Information and Communications, with the function of advising and assisting the Minister in implementing the management of foreign relations, integration and international cooperation in the fields under the state management of the Ministry of Information and Communications.""",
    "vu_khoa_hoc_cong_nghe": """The Department of Science and Technology is an organization under the Ministry of Information and Communications, with the function of advising and assisting the Minister in implementing state management of science and technology and measurement standards quality and environmental protection in industries and fields under the management of the Ministry of Information and Communications.""",
    "vu_kinh_te_va_xa_hoi_so": """The Department of Digital Economy and Digital Society is an organization under the Ministry of Information and Communications, performing the function of advising and assisting the Minister on digital economy and digital society development; state management on electronic transactions according to the provisions of law.""",
    "vu_phap_che": """The Department of Legal Affairs is an organization under the Ministry of Information and Communications, with the function of advising and assisting the Minister in implementing state management by law in the field of information and communications and organizing implementation Carry out legal work according to the provisions of law.""",
}


def get_answer(question: str, chat_history: any, organization: str):
    question = normalize_replace_abbreviation_text(question)
    description = ""
    for k, v in vu_en.items():
        if organization == k:
            description = v
            break
    docs = get_results(question)

    response = final_rag_chain.invoke(
        {
            "question": question,
            "docs": docs,
            "organization": description,
            "chat_history": chat_history,
        }
    )
    print(response)
    return {"response": response}
