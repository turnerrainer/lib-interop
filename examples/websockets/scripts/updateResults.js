function appendText(newText){
	var textBox = document.getElementById("textbox");
	var currentText = textBox.value;
	textBox.value = currentText+ "\n" + newText;
}