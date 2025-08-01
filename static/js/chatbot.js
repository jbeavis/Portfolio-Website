async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    addMessage('You', message);
    input.value = '';

    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message');
    loadingDiv.innerHTML = `<span class="bot">Bot:</span> ...`;
    chat.appendChild(loadingDiv);

    const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    chat.removeChild(loadingDiv);
    addMessage('Bot', data.response);
}

function addMessage(sender, text) {
    const chat = document.getElementById('chat');
    const div = document.createElement('div');
    div.classList.add('message');

    const content = sender === 'Bot'
        ? DOMPurify.sanitize(marked.parse(text))
        : text;

    div.innerHTML = `<span class="${sender === 'You' ? 'user' : 'bot'}">${sender}:</span> ${content}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function resetChat() {
    fetch('/reset', { method: 'POST' })
        .then(() => {
            document.getElementById('chat').innerHTML = '';
        });
}

function handleKey(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        sendMessage();
    }
}
