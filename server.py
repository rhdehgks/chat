import asyncio;
import websockets;
 
connected_clients = set()

async def server(ws, path):
    connected_clients.add(ws)
    try:
        async for msg in ws:
            msg = msg.decode("utf-8")
            print(f"Msg from client: {msg}")
            
            for client in list(connected_clients):
                print(client, ws)
                if client is not ws:
                    await client.send(msg)
    finally:
        connected_clients.remove(ws)

start_server = websockets.serve(server, "0.0.0.0", 5000)
print("Server started")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()