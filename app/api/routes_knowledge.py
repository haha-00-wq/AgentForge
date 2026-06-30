from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class KnowledgeQueryRequest(BaseModel):
    """知识库查询请求体。

    入参字段:
        question: 用户问题。
        limit: 最多检索切片数量。
    """

    question: str = Field(..., min_length=1)
    limit: int = Field(default=3, ge=1, le=10)


@router.post("/{kb_id}/files")
async def upload_knowledge_file(kb_id: str, request: Request, file: UploadFile = File(...)):
    """上传知识库文件。

    入参:
        kb_id: 知识库 ID。
        request: FastAPI 请求对象，用于访问共享 knowledge_base store。
        file: 上传文件，当前按 UTF-8 文本读取。

    出参:
        dict: 包含 kb_id、filename、chunks。

    异常:
        HTTPException(400): 文件不是 UTF-8 文本或内容为空时返回。
    """
    raw = await file.read()
    try:
        content = raw.decode("utf-8")
        documents = request.app.state.container.knowledge_base.add_text_file(kb_id, file.filename or "upload.txt", content)
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="Only UTF-8 text files are supported in the demo.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"kb_id": kb_id, "filename": file.filename, "chunks": len(documents)}


@router.post("/{kb_id}/query")
def query_knowledge_base(kb_id: str, body: KnowledgeQueryRequest, request: Request):
    """查询知识库。

    入参:
        kb_id: 知识库 ID。
        body: 查询请求体，包含 question 和 limit。
        request: FastAPI 请求对象，用于访问 workflow 注册表。

    出参:
        WorkflowResult: knowledge_base_qa_v1 的结构化问答结果。
    """
    workflow = request.app.state.container.workflows.get("knowledge_base_qa_v1")
    return workflow.run({"kb_id": kb_id, "question": body.question, "limit": body.limit})

