document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("sendButton");
    const messageInput = document.getElementById("messageInput");
    const messages = document.getElementById("messages");

    if (!sendButton || !messageInput || !messages) {
        console.error("Required DOM elements are missing!");
        return; // Prevent further script execution if any element is missing
    }

    const ws = new WebSocket("ws://localhost:8000/chat/1");

    ws.onopen = function() {
        console.log("WebSocket connection established");
    };

    ws.onmessage = function(event) {
        const message = document.createElement("div");
        message.textContent = event.data;
        messages.appendChild(message);
    };

    ws.onerror = function(error) {
        console.error("WebSocket error: ", error);
    };

    ws.onclose = function() {
        console.log("WebSocket connection closed");
    };

    sendButton.onclick = function() {
        if (messageInput.value.trim() !== "") {
            ws.send(messageInput.value);
            messageInput.value = ""; // Clear the input field
        }
    };
});
