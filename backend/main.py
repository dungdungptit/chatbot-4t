"""Main entrypoint for the app."""

import asyncio
from typing import Optional, Union
from uuid import UUID
from typing import Dict, List, Optional, Sequence, Tuple
import json
import langsmith
from fastapi.encoders import jsonable_encoder

# from chain import ChatRequest, answer_chain
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langsmith import Client
from pydantic import BaseModel
from chain_code import (
    get_answer,
    get_results,
    standard_name,
    search_standard,
    final_rag_chain,
    get_results_with_rewrite,
    ChatRequest,
)
from chain_sql import get_sql

# client = Client()

app = FastAPI()
app.search_results = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# add_routes(
#     app,
#     final_rag_chain,
#     path="/chat",
#     input_type=ChatRequest,
#     config_keys=["metadata", "configurable", "tags"],
# )


class SendFeedbackBody(BaseModel):
    run_id: UUID
    key: str = "user_score"

    score: Union[float, int, bool, None] = None
    feedback_id: Optional[UUID] = None
    comment: Optional[str] = None


# @app.post("/feedback")
# async def send_feedback(body: SendFeedbackBody):
#     client.create_feedback(
#         body.run_id,
#         body.key,
#         score=body.score,
#         comment=body.comment,
#         feedback_id=body.feedback_id,
#     )
#     return {"result": "posted feedback successfully", "code": 200}


class UpdateFeedbackBody(BaseModel):
    feedback_id: UUID
    score: Union[float, int, bool, None] = None
    comment: Optional[str] = None


# @app.patch("/feedback")
# async def update_feedback(body: UpdateFeedbackBody):
#     feedback_id = body.feedback_id
#     if feedback_id is None:
#         return {
#             "result": "No feedback ID provided",
#             "code": 400,
#         }
#     client.update_feedback(
#         feedback_id,
#         score=body.score,
#         comment=body.comment,
#     )
#     return {"result": "patched feedback successfully", "code": 200}


# TODO: Update when async API is available
async def _arun(func, *args, **kwargs):
    return await asyncio.get_running_loop().run_in_executor(None, func, *args, **kwargs)


# async def aget_trace_url(run_id: str) -> str:
#     for i in range(5):
#         try:
#             await _arun(client.read_run, run_id)
#             break
#         except langsmith.utils.LangSmithError:
#             await asyncio.sleep(1**i)

#     if await _arun(client.run_is_shared, run_id):
#         return await _arun(client.read_run_shared_link, run_id)
#     return await _arun(client.share_run, run_id)


class GetTraceBody(BaseModel):
    run_id: UUID


# @app.post("/get_trace")
# async def get_trace(body: GetTraceBody):
#     run_id = body.run_id
#     if run_id is None:
#         return {
#             "result": "No LangSmith run ID provided",
#             "code": 400,
#         }
#     return await aget_trace_url(str(run_id))


# dung code
@app.get("/search_results")
async def search_results(question: str):
    res = get_results(question)
    # res = [i[0] for i in res]
    # print(res)
    for index in range(len(res)):
        for k, v in res[index].metadata.items():
            if type(v) is list:
                # print(k, v[0])
                res[index].metadata[k] = v[0]
    res = search_standard(res)
    # print(res)
    return {"result": "preprocessed successfully", "code": 200, "res": res}

@app.get("/search_results_with_organization")
async def search_results_with_organization(question: str = "Standard involved in Machine Learning", organization: str = "vu_khoa_hoc_cong_nghe"):
    print(f'question: {question}, organization: {organization}')
    # res = f'question: {question}, organization: {organization}'
    res = get_results_with_rewrite(question, organization)
    # res = [i[0] for i in res]
    # print(res)
    for index in range(len(res)):
        for k, v in res[index].metadata.items():
            if type(v) is list:
                # print(k, v[0])
                res[index].metadata[k] = v[0]
    res = search_standard(res)
    # print(res)
    return {"result": "preprocessed successfully", "code": 200, "res": res}


@app.post("/chain_code")
async def get_answer_code(
    body: ChatRequest = Body(
        examples=[
            {
                "question": "Standard involved in Machine Learning",
                "chat_history": [],
                "organization": "vu_khoa_hoc_cong_nghe",
            }
        ],
    )
):
    question = body.question
    chat_history = body.chat_history
    organization = body.organization
    # return body
    # print(body)
    res = get_answer(question, chat_history, organization)
    # print(res)
    sources = get_results(question)
    # print(sources)
    sources = [i for i in sources if i.metadata["name_en"] in res["response"]]
    for index in range(len(sources)):
        for k, v in sources[index].metadata.items():
            if type(v) is list:
                # print(k, v[0])
                sources[index].metadata[k] = v[0]
    sources = search_standard(sources)
    return {
        "result": "successfully",
        "status": 200,
        "output": res,
        "sources": sources,
    }
    # try:
    # except:
    #     res = "Hmm, tôi không chắc."
    #     return {"result": "error", "status": 500, "output": res}


def insert_tree_node(tree, node, metadata):
    """
    Hàm đệ quy để chèn một node từ cấu trúc 'tree' vào cây chính.
    Node cha cũng sẽ chứa metadata từ cây con trong metadata.
    """
    current = tree
    # print("Node", node)
    name = node['name']
    
    # Nếu node đã tồn tại, tiếp tục đi sâu vào cây con
    if name not in current:
        current[name] = {
            'metadata': {
                'name': node['name'],
                'display_name': node.get('display_name'),
                'description': node.get('description'),
                'parrent': node.get('parrent')
            },
            'children': {},
            'leaf_count': 0,  # Sẽ dùng để đếm các node lá
            'list_data': []
        }
    
    # Nếu node có con, tiếp tục đệ quy với cây con
    if 'children' in node and node['children']:
        # print("Children", node['children'])
        for child in node['children']:
            # print("Child", child)
            insert_tree_node(current[name]['children'], child, metadata)
    else:
        # Nếu node không có con, đó là node cuối cùng -> thêm metadata
        # print(metadata)
        current[name]['list_data'].append(metadata)

def count_all_leaf_nodes(tree):
    """
    Hàm đệ quy để đếm tổng số node lá trong cây (những node cuối cùng không có con).
    """
    total_leaves = 0
    
    for node, value in tree.items():
        # Nếu node có con, đệ quy vào cây con để đếm tổng số lá của cây đó
        if value['children']:
            value['leaf_count'] = count_all_leaf_nodes(value['children'])
        else:
            # Nếu là node lá, gán leaf_count là 1
            value['leaf_count'] = 1
        
        # Cộng dồn số node lá
        total_leaves += value['leaf_count']
    
    return total_leaves

def count_records_by_standard_organisation(sources: list):
    organisation_standards = ["3GPP", "ETSI", "ITU", "ANSI", "ISO/IEC", "IEC/ISO", "ISO/TC", "ISO/PC", "ISO/WS"]
    general_organisation_standards = ["3GPP", "ETSI", "ANSI", "ISO", "ITU", "IEC"]
    reports = {"Other": 0}
    standards = []
    for organisation in general_organisation_standards:
        reports[organisation] = 0
    for standard in sources:
        branch = standard.metadata["branch"]
        # print(standard.metadata, branch)
        standards.append(standard.metadata["id"])
        for organisation in general_organisation_standards:
            is_check = False
            if not branch:
                if organisation in standard.metadata['id']:
                    reports[organisation] += 1
                    is_check = True
                    break
            elif organisation in branch:
                reports[organisation] += 1
                is_check = True
                break
        if not is_check:
            print(branch, standard.metadata['id'])
            reports["Other"] += 1
    # print(len(sources), standards)
    print(reports)
    return reports

@app.post("/chain_code_tree")
async def get_answer_code(
    body: ChatRequest = Body(
        examples=[
            {
                "question": "Standard involved in Machine Learning",
                "chat_history": [],
                "organization": "vu_khoa_hoc_cong_nghe",
            }
        ],
    )
):
    question = body.question
    chat_history = body.chat_history
    organization = body.organization
    # return body
    # print(body)
    res = get_answer(question, chat_history, organization)
    # print(res)
    sources = get_results(question)
    # sources = sources[:20]
    # print(sources)
    # sources = [i for i in sources if i.metadata["name_en"] in res["response"]]
    reports = count_records_by_standard_organisation(sources)
    # for index in range(len(sources)):
    #     for k, v in sources[index].metadata.items():
    #         if type(v) is list:
    #             # print("Meta", k, v[0])
    #             sources[index].metadata[k] = v[0]
    # sources = search_standard(sources)
    # # data = [[j.strip() for j in i.metadata['branch'].split("->")] for i in sources]
    
    # # Cấu trúc cây dữ liệu
    # tree = {}
    
    # # Chèn dữ liệu vào cây
    # for entry in sources:
    #     if len(entry.metadata['tree'].keys()):
    #         insert_tree_node(tree, entry.metadata['tree'], entry.metadata)

    # # Đếm tổng số node lá
    # count_all_leaf_nodes(tree)
    # print(json.dumps(tree, indent=4))
    # print(tree)
    # print(tree)
    response = {
        "result": "successfully",
        "status": 200,
        "report": reports
        # "tree": json.dumps(tree, indent=4)
    }
    app.search_results = sources
    return response
    # try:
    # except:
    #     res = "Hmm, tôi không chắc."
    #     return {"result": "error", "status": 500, "output": res}

@app.post("/chain_code_top_tree")
async def get_answer_code_top_k(
    k: int
):
    sources = app.search_results
    sources = sources[:k]
    reports = count_records_by_standard_organisation(sources)
    for index in range(len(sources)):
        for k, v in sources[index].metadata.items():
            if type(v) is list:
                # print("Meta", k, v[0])
                sources[index].metadata[k] = v[0]
    sources = search_standard(sources)
    # data = [[j.strip() for j in i.metadata['branch'].split("->")] for i in sources]
    
    # Cấu trúc cây dữ liệu
    tree = {}
    
    # Chèn dữ liệu vào cây
    for entry in sources:
        if len(entry.metadata['tree'].keys()):
            insert_tree_node(tree, entry.metadata['tree'], entry.metadata)

    # Đếm tổng số node lá
    count_all_leaf_nodes(tree)
    # print(json.dumps(tree, indent=4))
    # print(tree)
    # print(tree)
    response = {
        "result": "successfully",
        "status": 200,
        "sources": sources,
        "tree": tree
        # "tree": json.dumps(tree, indent=4)
    }
    return response
    # try:
    # except:
    #     res = "Hmm, tôi không chắc."
    #     return {"result": "error", "status": 500, "output": res}


@app.get("/chain_sql")
async def get_answer_sql(question: str):
    res = get_sql(json.dumps(question, ensure_ascii=True))
    return {"result": "preprocessed successfully", "code": 200, "query": res}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
