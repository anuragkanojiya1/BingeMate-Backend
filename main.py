# main.py
from fastapi import FastAPI, Query, Request
from typing import Optional, Dict
from mindsdb_client import query_knowledge_base, query_agent
from pydantic import BaseModel

app = FastAPI(title="MindsDB Knowledge Base API")

@app.get("/")
def root():
    return {"message": "MindsDB Query API is running."}

@app.get("/query")
def search_kb(
    request: Request,
    q: str = Query(..., description="Search query, e.g., 'best netflix series'"),
    min_relevance: float = Query(0.25, description="Minimum relevance threshold"),
    # metadata: Optional[Dict[str, str]] = None
):
    query_params = dict(request.query_params)

    query_params.pop("q", None)
    query_params.pop("min_relevance", None)
    results = query_knowledge_base(search_query=q, min_relevance=min_relevance, metadata=query_params)
    return {"count": len(results), "results": results}

@app.post("/api/projects/mindsdb/jobs")
def create_job(
    project: str = Query(..., description="Project name"),
    job_name: str = Query(..., description="Job name"),
    query: str = Query(..., description="SQL query to execute")
):
    return {
        "message": f"Job '{job_name}' created in project '{project}' with query: {query}"
    }

@app.get("/agent")
def create_agent(
    query: str = Query(..., description="Question to ask the agent"),
    description: Optional[str] = Query(None, description="Description of the agent")
):
    result = query_agent(query=query)
    return {
        "result": result
        }