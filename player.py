from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,APIRouter
import asyncio



playerRouter = APIRouter()

active_connections: dict[str, List[WebSocket]] = {}
saved_message = None


async def connect(websocket: WebSocket, room_id: str) -> bool:
    await websocket.accept()
    if room_id in active_connections:
        if len(active_connections[room_id]) < 2:  # Ensure only 2 players per room
            active_connections[room_id].append(websocket)

        
        
        return True
    else:
        active_connections[room_id] = [websocket]
        return True
    return False

def disconnect(websocket: WebSocket, room_id: str):
    global saved_message
    if room_id in active_connections:
        active_connections[room_id].remove(websocket)
        if len(active_connections[room_id]) == 0:
            del active_connections[room_id]
            saved_message=None

async def broadcast(message: str, room_id: str):
    if room_id in active_connections:
        for connection in active_connections[room_id]:
            await connection.send_text(message)


@playerRouter.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    global saved_message
    if not await connect(websocket, room_id):
        await websocket.close(code=1003)  # Close connection if room is full
        return
    
    if saved_message is None:
                saved_message=await websocket.receive_text()
                await broadcast(saved_message,room_id)
                await websocket.send_text("X")
    else:
            await broadcast(saved_message,room_id)
            await websocket.send_text("O")
            if(len(active_connections[room_id])==2):
               await broadcast("ready",room_id)
    


    try:
        while True:
             data=await websocket.receive_text()
             await broadcast(data,room_id)
            
    except WebSocketDisconnect:
        disconnect(websocket, room_id)
        await broadcast(f"A player has left the room {room_id}.", room_id)


