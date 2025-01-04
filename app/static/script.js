const ws = new WebSocket("ws://localhost:8000/ws/chat/1");

ws.onmessage = function(event) {
    const messages = document.getElementById("messages");
    const message = document.createElement("div");
    message.textContent = event.data;
    messages.appendChild(message);
};

document.getElementById("sendButton").onclick = function() {
    const input = document.getElementById("messageInput");
    ws.send(input.value);
    input.value = "";
};
