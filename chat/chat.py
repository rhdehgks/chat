from fastapi import APIRouter, WebSocket
import uuid
from typing import Dict, List

router = APIRouter()

clients: Dict[str, WebSocket] = {}

@router.on_event("startup")
async def init():
    pass

@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    account = await websocket.receive_json()
    if account['id']:
        id = account['id']
        if id in clients:
            await websocket.close(code=4000, reason= "이미 접속중인 계정입니다.")
            return
    else:
        print('신규등록')
        id = str(uuid.uuid4())
        await register(id, websocket)
    nickname = account['nickname']
    connect(id, websocket)
    print(f"id: {id}, nickname: {nickname}")
    try:
        while True:
            data = await websocket.receive_json()

            data['id'] = id
            data['nickname'] = nickname
            for _, ws in clients.items():
                await ws.send_json(data)
    finally:
        disconnect(id)

async def register(id: str, websocket: WebSocket):
    await websocket.send_json({'id': id})
    await websocket.receive_json()

def connect(id: str, websocket: WebSocket):
    clients[id] = websocket

def disconnect(id: str):
    clients.pop(id)