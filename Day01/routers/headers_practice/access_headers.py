from fastapi import APIRouter, Request, Header
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

@router.get('/show_current_headers/')
async def show_current_headers(request: Request):
    headers = request.headers
    return {
        "headers": dict(headers)
    }

@router.post('/set_headers/')
async def getting_headers(
    user_agent: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    connection: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
):
    request_headers = {}
    request_headers["User-Agent"] = user_agent
    request_headers["Accept-Encoding"] = accept_encoding
    request_headers["Referer"] = referer
    request_headers["Accept-Language"] = accept_language
    request_headers["Connection"] = connection
    request_headers["Host"] = host

    return request_headers
    
