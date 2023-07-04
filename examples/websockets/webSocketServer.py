import asyncio
import websockets
import whisper

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
                #process_audio_stream(audio_data)
                print("Received audio stream length:", len(audio_data))
                with open('received_audio.wav', 'wb') as audio_file:
                   audio_file.write(audio_data)
                   print("Audio file saved successfully")
                   result = transcribe_file("received_audio.wav")
                   transcription = result
                   print(transcription)
                   print(result)
                '''
                # Check if the complete audio data should be processed
                if should_process_complete_audio(audio_data):
                    # Process the complete audio data
                    process_complete_audio(audio_data)
                    print("processed audio")
                    # Send a response to the client
                    await websocket.send(transcription)
				
                '''
                await websocket.send(transcription)
                # Send another audio file back to the client
                with open('testFile.wav', 'rb') as audio_file:
                    await websocket.send(audio_file.read())
                    
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print("Error:", e)

def process_audio_stream(audio_data):
    # Process the received audio stream as needed
    # Here, we simply print the length of the received audio data
    print("Received audio stream length:", len(audio_data))
    process_complete_audio(audio_data)

def should_process_complete_audio(audio_data):
    # Determine if the complete audio data should be processed
    # Here, we assume that a specific condition triggers the processing
    return audio_data.endswith(b'complete')

async def process_complete_audio(audio_data):
    # Process the complete audio data as needed
    # Here, we save it to an audio file named 'audio_file_received.wav'
    with open('received_audio.wav', 'wb') as audio_file:
        audio_file.write(audio_data)
    print("Audio file saved successfully")
    result = transcribe_file("received_audio.wav")
    transcription = result
    print(transcription)
    print(result)
    
	
def transcribe_file(name):
    model = whisper.load_model("base.en")
    result = model.transcribe(name)
    transcription = result["text"]
    return(transcription)
    #print(result["text"])


# Create a WebSocket server
start_server = websockets.serve(audio_server, 'localhost', 8765)

# Start the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()