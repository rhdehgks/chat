import asyncio;
import websockets;
 
async def server(ws, path):
    async for msg in ws:
        msg = msg.decode("utf-8")
        print(f"Msg from client: {msg}")
        await ws.send(f"{msg}")

start_server = websockets.serve(server, "13.125.159.144", 5000)
print("Server started")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()