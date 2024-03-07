# import asyncio
# import websockets

# async def echo_handler(websocket, path):
#     try:
#         async for message in websocket:
#             print(f"Received message from client: {message}")

#             # Process the message if needed
#             processed_message = f"Server processed: {message}"

#             # Echo the processed message back to the client
#             await websocket.send(processed_message)
#             print(f"Sent message back to client: {processed_message}")

#     except websockets.exceptions.ConnectionClosed:
#         print(f"Client disconnected: {websocket.remote_address}")

# async def main():
#     server_address = "192.168.100.39"
#     server_port = 8000

#     # Create the WebSocket server
#     server = await websockets.serve(
#         echo_handler,
#         server_address,
#         server_port
#     )

#     print(f"WebSocket server started at ws://{server_address}:{server_port}")

#     try:
#         # Run the server forever
#         await server.wait_closed()
#     except KeyboardInterrupt:
#         print("Server stopped")

# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(main())
# First, install plyer by using pip
# pip install plyer

from plyer import notification

notification.notify(
    title="Sample Notification",
    message="This is a sample notification",
    timeout=10
)
