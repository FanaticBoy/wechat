import asyncio
import time

import websockets

# 用于存储所有连接的客户端
connected_clients = set()



# 处理客户端连接的协程
async def handle_client(websocket, path):
    # 将新连接的客户端添加到已连接的客户端集合中
    connected_clients.add(websocket)
    print(path)


    try:
        while True:
            # 接收客户端发送的消息
            message = await websocket.recv()
            print(f"Received message: {message}")

            # 生成消息id
            message_id = int(path[1:])

            message_with_id = message_id
            # await websocket.send(message_with_id)



            # 广播消息给所有连接的客户端
            for client in connected_clients:
                await client.send(f"{message_with_id}:{message}")

            online_count = len(connected_clients)
            online_count_message = f"Online Count: {online_count}"
            for client in connected_clients:
                if not client.closed:
                    await client.send(online_count_message)
    except websockets.exceptions.ConnectionClosed:
        # 当客户端断开连接时，从已连接的客户端集合中移除
        connected_clients.remove(websocket)
        for client in connected_clients:
            await client.send(f"{int(path[1:])}已退出")
            online_count = len(connected_clients)
            online_count_message = f"Online Count: {online_count}"
            await client.send(online_count_message)
    finally:
        pass



async def main():
    async with websockets.serve(handle_client, "localhost", 8000, ping_interval=None):
        await asyncio.Future()  # run forever


asyncio.run(main())
