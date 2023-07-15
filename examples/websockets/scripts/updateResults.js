function appendText(messageWindow,newText){
    console.log(messageWindow);
	var textBox = document.getElementById(messageWindow);
    console.log(textBox);
	var currentText = textBox.value;
	textBox.value = currentText+ "\n" + newText;
}

function decideMessageType(message){
    var messageType;
    if(message.startsWith("dialog event:")){
        messageType = "dialogEvent";
    }
    else{
        messageType = "conversationTurn";
    }
   
    return messageType;
}