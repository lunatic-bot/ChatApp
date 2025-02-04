document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("sendButton");
    const messageInput = document.getElementById("messageInput");
    const messages = document.getElementById("messages");

    if (!sendButton || !messageInput || !messages) {
        console.error("Required DOM elements are missing!");
        return;
    }

    function connectWebSocket() {
        let ws = new WebSocket("ws://localhost:8000/chat/1");

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
            console.log("WebSocket connection closed. Reconnecting in 3 seconds...");
            setTimeout(connectWebSocket, 3000);
        };

        sendButton.onclick = function() {
            if (messageInput.value.trim() !== "" && ws.readyState === WebSocket.OPEN) {
                ws.send(messageInput.value);
                messageInput.value = "";
            } else {
                console.warn("WebSocket is not open. Cannot send message.");
            }
        };

        return ws;
    }

    // Ensure only one WebSocket connection
    if (!window.chatSocket || window.chatSocket.readyState !== WebSocket.OPEN) {
        window.chatSocket = connectWebSocket();
    }
});
