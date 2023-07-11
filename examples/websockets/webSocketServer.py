import asyncio
import websockets
import whisper
import assistant
from gtts import gTTS

transcription = "initial transcription"

async def audio_server(websocket, path):
    try:
        while True:
            audio_data = b''
            
            # Receive data from the client
            while True:
                data = await websocket.recv()
                if data == 'end_stream':
                    break
                audio_data += data
               
            if audio_data:
                # Process the audio stream as needed
                print("Received audio stream length:", len(audio_data))
                with open('received_audio.wav', 'wb') as audio_file:
                   audio_file.write(audio_data)
                   print("Audio file saved successfully")
                   result = transcribe_file("received_audio.wav")
                   transcription = result
                   print(transcription)
                   print(result)
                   what_to_say = assistant.assistant(transcription)
                   print(what_to_say)
              
                await websocket.send(transcription)
                print("transcription received by client")
                # Send assistant response audio back to the client
                output_audio = gTTS(what_to_say)
                output_audio.save("output_audio_file.wav")
                with open("output_audio_file.wav", 'rb') as audio_file:
                    await websocket.send(audio_file.read())
                await websocket.send(what_to_say)
                                 
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print("Error:", e)


    
def transcribe_file(name):
    print("transcribing file")
    print(name)
    print("loading model")
    model = whisper.load_model("base.en")
    print("loaded model")
    result = model.transcribe(name)
    print("transcribed file")
    transcription = result["text"]
    return(transcription)
    #print(result["text"])


# Create a WebSocket server
start_server = websockets.serve(audio_server, 'localhost', 8765)

# Start the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()