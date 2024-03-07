import asyncio
import websockets


async def handle_audio(websocket, path):
    try:
        async for audio_data in websocket:
            # Assuming the audio data is received as binary
            # You can implement the logic to store the audio data to a file storage system here
            with open("recorded_audio.wav", "wb") as f:
                f.write(audio_data)
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed unexpectedly")


start_server = websockets.serve(handle_audio, "192.168.100.39", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
