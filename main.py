import uvicorn 
import asyncio 
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

@app.get("/")
def test():
    return {"test message:": "bitch"}


connected_users = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept() 
    connected_users[user_id] = websocket  
    
    try:
        while True:
            data = await websocket.receive_text()
            for user, user_ws in connected_users.items():
                ret = f"{user_id}: {data}"
                await user_ws.send_text(ret)
    except Exception as exc:
        print("Error", exc)
        del connected_users[user_id]
        await websocket.close()
        
@app.websocket("ws/log-reader")
async def log_reader(websocket: WebSocket):
    await websocket.accept() 
    try:
        while True:
            asyncio.sleep(1)
            data = None 
            await websocket.send_text(data)
    except Exception as exc:
        print("Error in log reading", exc)
        await websocket.close()
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)