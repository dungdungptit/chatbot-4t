"""Main entrypoint for the app."""

import asyncio
from typing import Optional, Union
from uuid import UUID
from typing import Dict, List, Optional, Sequence, Tuple

import langsmith

# from chain import ChatRequest, answer_chain
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langsmith import Client
from pydantic import BaseModel
from chain_code import get_answer, get_results, final_rag_chain, ChatRequest
from chain_sql import get_sql

# client = Client()

app = FastAPI()
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
    print(body)
    res = get_answer(question, chat_history, organization)
    print(res)
    return {
        "result": "successfully",
        "status": 200,
        "output": res,
        "sources": get_results(question),
    }
    # try:
    # except:
    #     res = "Hmm, tôi không chắc."
    #     return {"result": "error", "status": 500, "output": res}


@app.get("/chain_sql")
async def get_answer_sql(question: str):
    res = get_sql(question)
    return {"result": "preprocessed successfully", "code": 200, "query": res}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
