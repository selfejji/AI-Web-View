require('dotenv').config();

const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const injectionTarget = document.getElementById('injection-target');
const placeholderContent = document.querySelector('.placeholder-content');

// --- Chat Agent Logic ---
sendBtn.addEventListener('click', async () => {
    const prompt = chatInput.value.trim();
    if (!prompt) return;

    // Hide chat box AND placeholder content
    chatContainer.classList.add('hidden');
    if (placeholderContent) {
        placeholderContent.classList.add('hidden');
    }

    injectionTarget.innerHTML = '<p>Agent is generating code...</p>';

    try {
        // Inside your script.js click listener:
        const response = await fetch(CONFIG.OPEN_WEBUI_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${CONFIG.AGENT_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "CCS AI",
                messages: [{ role: 'user', content: prompt }]
            })
        });

        const data = await response.json();
        const injectedCode = data.choices[0].message.content;
        
        // Inject the generated response into the page
        injectionTarget.innerHTML = `<div>${injectedCode}</div>`;

    } catch (error) {
        injectionTarget.innerHTML = `<p style="color:red;">Error connecting to agent: ${error.message}</p>`;
        
        // Bring UI elements back if the connection fails
        chatContainer.classList.remove('hidden');
        if (placeholderContent) {
            placeholderContent.classList.remove('hidden');
        }
    }
});