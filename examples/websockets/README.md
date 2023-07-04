# Demonstration of using websockets to do server-side speech recognition and TTS
The client is a web browser and the server is a websocket server
The ASR and TTS are done on the primary assistant.
This could be used for the channeling pattern.

## Server-side code (Python):
1. webSocketServer.py (primary assistant)
2. Start the server at the command line with "python webSocketServer.py"
3. The server is setup to run on localhost, port 8765
4. waits for audio to be sent over a websocket
5. when it receives the audio, it transcribes it with the open source OpenAI Whisper ASR software, which must be installed on the server, but which doesn't require internet access.
6. More information about Whisper and instructions for installing can be found at https://github.com/openai/whisper. Note that Whisper can be configured to use many models and supports many languages.
7. After the audio is transcribed, the transcription is returned to the client, where it is displayed in a browser window.

## Client-side code (HTML/Javascript):
### sendAudioToServer.html
1. Click on "start listening" to start streaming audio to the server
2. Give the application permission to use the microphone
3. Speak your request
4. Click "Stop listening" when finished speaking
5. The result will be displayed in the textarea in the browser

### captureAudio.js
1. sends the audio stream to the server
2. waits for the transcription from the server and updates the results

### updateResults.js
1. updates the textarea with the transcription

## todo:
1. receive and play TTS audio from the server (possible TTS could be TesnorFlowTTS, version fastspeech2, just the inference code is necessary since we aren't training the TTS)
2. write a rudimentary discovery placeholder
3. write a rudimentary secondary assistant that accepts OVON messages from the server
4. connect to the secondary assistant from the server
5. format the transcription as an OVON message and send it to the secondary assistant, that responds
6. send the secondary assistant's response via TTS back to the client



