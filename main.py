import os
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="echo-ai-agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    prompt: str = Field(min_length=1)
    stream: bool = False


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "echo-ai-agent", "version": "1.0.0"}


@app.get("/metadata")
async def metadata() -> dict[str, str | list[str]]:
    return {
        "name": "echo-ai-agent",
        "version": "1.0.0",
        "framework": "FastAPI",
        "capabilities": ["text-generation", "task-execution"],
    }


@app.post("/execute")
async def execute(request: ExecuteRequest) -> dict[str, str | list[str]]:
    return {
        "agent_id": str(uuid4()),
        "prompt": request.prompt,
        "response": f"Echo: {request.prompt}",
        "thoughts": ["Received the prompt", "Generated an echo response"],
        "status": "completed",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
