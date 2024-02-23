import asyncio
import websockets

async def send_ping(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                await websocket.ping()
                print("Ping sent to", uri)
                await asyncio.sleep(5)  # Send ping every 5 seconds
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed unexpectedly.")
                break
            except Exception as e:
                print("Error:", e)
                break

# Replace 'wss://fgram.foxdev.uz/' with your WebSocket URL
websocket_uri = 'wss://fgram.foxdev.uz/'
asyncio.run(send_ping(websocket_uri))
