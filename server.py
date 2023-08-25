import asyncio;
import websockets;
import random;
 
connected_clients = set()
words = {
    '나그네', '거북이', '사람', '누구게', '아무개', '홍길동', '외계인'
}
names = dict()

async def server(ws, path):
    connected_clients.add(ws)
    names[ws] = words.pop()
    for client in list(connected_clients):
        await client.send(f"{names[ws]}님이 입장하였습니다.")
    try:
        async for msg in ws:
            msg = msg.decode("utf-8")
            print(f"Msg from client: {msg}")
            for client in list(connected_clients):
                if client is ws:
                    await client.send(f"[color=green]{names[ws]}[/color]: {msg}")
                else:
                    await client.send(f"{names[ws]}: {msg}")
    finally:
        words.add(names[ws])
        del names[ws]
        connected_clients.remove(ws)

start_server = websockets.serve(server, "0.0.0.0", 5000)
print("Server started")
print(words)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()