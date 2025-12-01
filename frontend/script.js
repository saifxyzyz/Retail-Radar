document.addEventListener('DOMContentLoaded', () => {
    const startAnalysisBtn = document.getElementById('start-analysis');
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
        statusDiv.textContent = 'Connected to the server.';
    };

    socket.onmessage = (event) => {
        resultsDiv.innerHTML += event.data.replace(/\n/g, '<br>');
    };

    socket.onclose = () => {
        statusDiv.textContent = 'Disconnected from the server.';
    };

    socket.onerror = (error) => {
        console.error('WebSocket Error:', error);
        statusDiv.textContent = 'An error occurred with the connection.';
    };

    startAnalysisBtn.addEventListener('click', () => {
        statusDiv.textContent = 'Starting analysis...';
        resultsDiv.innerHTML = '';
        
        fetch('http://localhost:8000/start-analysis', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                statusDiv.textContent = 'An error occurred.';
                resultsDiv.innerHTML = `<p>Error: ${data.message}</p>`;
            }
        })
        .catch(error => {
            statusDiv.textContent = 'An error occurred.';
            console.error('Error:', error);
        });
    });
});

