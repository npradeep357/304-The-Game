document.addEventListener('DOMContentLoaded', () => {
    const gameStatusDiv = document.getElementById('game-status');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const receivedMessagesDiv = document.getElementById('received-messages');

    // Replace with your actual WebSocket URL and session ID
    const websocketUrl = 'ws://localhost:8000/ws/test_session_id';
    let websocket;

    function connectWebSocket() {
        websocket = new WebSocket(websocketUrl);

        websocket.onopen = (event) => {
            console.log('WebSocket connected:', event);
            gameStatusDiv.textContent = 'Connected to game session.';
        };

        websocket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            const messageElement = document.createElement('p');
            messageElement.textContent = `Received: ${event.data}`;
            receivedMessagesDiv.appendChild(messageElement);
        };

        websocket.onerror = (event) => {
            console.error('WebSocket error:', event);
            gameStatusDiv.textContent = 'WebSocket error. Check console.';
        };

        websocket.onclose = (event) => {
            console.log('WebSocket closed:', event);
            gameStatusDiv.textContent = 'WebSocket disconnected.';
            // Attempt to reconnect after a delay
            setTimeout(connectWebSocket, 1000);
        };
    }

    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(message);
            console.log('Sent message:', message);
            messageInput.value = ''; // Clear input after sending
        } else {
            console.error('WebSocket is not connected.');
            gameStatusDiv.textContent = 'WebSocket not connected. Cannot send message.';
        }
    });

    // Initial connection
    connectWebSocket();
});