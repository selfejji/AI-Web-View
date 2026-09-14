import httpx
import os
import uuid
from pydantic import BaseModel, Field
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from tools.py import *
from content_post.py import *
from content_grab.py import *

# 1. Initialize the FastAPI application
app = FastAPI(
    title="Web View",
    description="An AI centered microservice that empowers users to create reports, graphs/charts, and basic calculators as an interfaceable web application.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any frontend origin during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration 
OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_BASE_URL")
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")
TAG = os.getenv("COMPATABILITY")
CURRENT_SESSION_ID = str(uuid.uuid4())
security = HTTPBearer()


#--------------------#
#
# System getter definitions
#
#--------------------#

async def getHeaders():
    return {
        "Authorization": f"Bearer {OPEN_WEBUI_API_KEY}",
        "Content-Type": "application/json"
    }


#--------------------#
#
# Class definitions
#
#--------------------#

class Params(BaseModel):
    # variable
    paramType: str
    model: str = ""
    usrPrompt: str = ""
    chat_id: str = ""
    sessionId: str = ""

    # static
    tools: list[str] = Field(default_factory=list)

    async def returnParam(self):
        # Default to instance's paramType if not explicitly passed
        target_type = self.paramType

        try:
            if not target_type or "stream" not in target_type:
                raise ValueError(
                    f"'{target_type}' is not an established param type"
                )

            if target_type == "stream":
                payload = {
                    "model": self.model,
                    "chat_id": self.chat_id,
                    "stream": True,
                    "messages": [{"role": "user", "content": self.usrPrompt}],
                    "tool_ids": self.tool_ids,
                    "metadata": {"session_id": self.sessionId},
                }

            return payload

        except Exception as e:
            print(f"No such params: {e}") 
            return None

# Request body structure coming from JS
class ChatRequest(BaseModel):
    model: str
    usrPrompt: str
    chat_id: str


#--------------------#
#
# Endpoint Constructions
#
#--------------------#

@app.get("/api/v1/models/export", response_model = List[Dict[str, Any]])
async def get_custom_agents():
    url = f"{OPEN_WEBUI_URL}/api/v1/models/export"
    headers = await getHeaders()

    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = headers, timeout = 10.0)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code = response.status_code, 
                    detail = f"Open WebUI API returned an error: { response.text }"
                )
                return
                
            payload = response.json().get("data", [])

#            Filter the "data" array inside the payload, retaining all outer metadata
            payload["data"] = [
                model for model in payload.get("data", [])
                if TAG in [
                    t.get("name") if isinstance(t, dict) else t
                    for t in (((model.get("info") or {}).get("meta") or {}).get("tags") or [])
                    if t
                ]
            ]

            return payload
            
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503, 
                detail=f"Could not connect to Open WebUI server: { exc }"
            )
            return

async def get_agent_response():
    url = f"{OPEN_WEBUI_URL}/api/chat/completions"
    headers = await getHeaders()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = headers, stream = True, timeout = 10.0)

            if response.status_code != 200:
                raise HTTPException(
                    status_code = response.status_code,
                    detail = f"Open WebUI API returned an error: { response.text }"
                )
                return
            
            agent_response = response.json().get("data", [])

            return agent_response
    
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code = 503,
                detail = f"Could not connect to Open WebUI server: { exc }"
            )
            return

@app.post("/api/chat/completions")
async def chat_session(req: ChatRequest):
    url = f"{OPEN_WEBUI_URL}/api/chat/completions"
    headers = await getHeaders()

    params = Params(
        paramType = "stream", 
        model = req.model,
        usrPrompt = req.usrPrompt,
        chat_id = req.chat_id,
        sessionId = CURRENT_SESSION_ID
    )

    payload = await params.returnParams()

    async with httpx.AsyncClient() as client:    
        try:
            if (payload is None): 
                raise Exception(f"Payload is null")
                return

            prompt = await client.post(url, json = payload, headers = headers, stream = True, timeout = 10.0)

            for line in prompt.iter_lines():
                if line:
                    print(line.decode("utf-8"))

            response = await get_agent_response()

            return { "message": response }

        except Exception as e:
            print("Not a valid payload: {e}")
            return

@app.post("/api/v1/files/")
async def upload_files(file_path):
    url = f"{OPEN_WEBUI_URL}/api/v1/files/"
    headers = await getHeaders()

    async with httpx.AsyncClient() as client:
        try:
            files = {'file': open(file_path, 'rb')}
            response = await client.post(url, headers = headers, files = files)

            if (response is None) : 
                raise Exception(f"file cannot be null")
                return
            return response.json()
        except Exception as e:
            print("Invalid file: {e}")
            return


