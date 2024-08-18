import uvicorn 
import asyncio 
import websockets 

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from typing import List

from helper import log_reader_helper
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

@app.websocket("/ws/chat-app/{user_id}")
async def chat_app(user_id: str, websocket: WebSocket):
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
        
@app.websocket("/ws/log-reader")
async def log_reader(websocket: WebSocket):
    await websocket.accept() 
    try:
        while True:
            await asyncio.sleep(1)
            data = log_reader_helper('test.log')
            print(data)
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("web socket disonnected")
    except websockets.exceptions.ConnectionClosedError:
        print("connection closed abruptly")
    except Exception as exc:
        print("Error in log reading", exc)
        await websocket.close()
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)