var socket;
var mediaRecorder


function startScript(){
// Creating a WebSocket connection
console.log("opening a socket")
socket = new WebSocket('ws://localhost:8765');
   console.log('WebSocket connection opened');
// Handle WebSocket connection open event
socket.binaryType = 'blob';
socket.onopen = event => {
    console.log("[open] websocket connection established");
    navigator.mediaDevices
        .getUserMedia({ audio: true, video: false })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=pcm',
            });
            mediaRecorder.addEventListener('dataavailable', event => {
                if (event.data.size > 0) {
					console.log("sending data")
                    socket.send(event.data);
                }
            });
            mediaRecorder.start(1000);
        });
};

// Handle WebSocket errors
socket.onerror = error => {
  console.error('WebSocket error:', error);
};

// Handle WebSocket message event

/*socket.onmessage = event => {
   console.log(event.data)
   appendText(event.data)
}
*/

socket.onmessage = function(event) {
  if (typeof event.data === 'string') {
    // Handle text data
    var receivedText = event.data;
    console.log("Received text:", receivedText);
	console.log(event.data)
    appendText(event.data);
    
    // Use the received text as needed
  } else if (event.data instanceof Blob) {
    // Handle Blob data (you can choose to ignore it if needed)
    // Create an audio element
       const audio = new Audio();
  
  // Set the received audio data as the audio source
       audio.src = URL.createObjectURL(event.data);
  
  // Play the audio
  audio.play();
  } else {
    // Handle other types of data (if applicable)
    console.log("Received data of unknown type");
  }
};
 

// Handle WebSocket connection close event
socket.onclose = () => {
  console.log('WebSocket connection closed');
};
}

function stopRecording(){
	console.log("finished recording");
	mediaRecorder.stop();
	socket.send("end_stream");
}

function closeSocket(){
    socket.close();
}



