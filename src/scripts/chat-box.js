/*
-- Owner: Sammy Elfejji
-- Camden County Schools Technology
--
-- #--- CCST Web View ---#
-- An AI centered microservice that empowers users to create 
-- reports, graphs/charts, and basic calculators as an interfaceable web application.
--
-- Date: 09/07/2026
*/

// Element definitions
const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const injectionTarget = document.getElementById('app');

// Parses document for most recent element that matches
const placeholderContent = document.querySelector('.placeholder-content');
const originalText = placeholderContent.textContent;
const placeholderContent_text = originalText;

// Event listener for the generate button for chat
sendBtn.addEventListener('click', async () => {
    const prompt = chatInput.value.trim(); // removes any unecessary whitespaces on beginning and end of user input
    if (!prompt) return;

    try {
        // Fetches the AI response from API
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

        // Creates AI response in both JSON and JS Object format
        const data = await response.json();
        const data_obj = JSON.parse(data);
        const codeRegex = /(function\s+\w+|.*?\s*=>|\b(const|let|var)\b|```[a-z]*\n|[\{\};])/g; // Regex definition for checkig if AI generated code

        try {
            // Checks if the oresponse contains generated code
            if(Object.values(data_obj).includes(codeRegex)) {

                // Removes placeholder
                if (placeholderContent) {
                    placeholderContent.classList.add('hidden');
                }

                // Creates injected code string
                const injectedCode = data.choices[0].message.content;
                injectionTarget.innerHTML = `<div>${injectedCode}</div>`;

                // MAKE APEAR IN view-container

            // Checks if response is not null but did not contain any code    
            } else if(!Object.values(data_obj).includes(codeRegex) && (data_obj && typeof data_obj === 'object')) {
                // Alerts user chat is in session.
                placeholderContent_text = "Chat is in session 🤖. Ask chat to generate something!";
                placeholderContent.textContent(placeholderContent_text);

                // Removes placeholder
                if (placeholderContent) {
                    placeholderContent.classList.remove('hidden');
                }

            } else {
                throw error;
            }
        } catch (error) {
            injectionTarget.innerHTML = `<p style="color:red;">Failed to generate response: ${error.message}</p>`;
            placeholderContent_text = "Chat is in session!";
            placeholderContent.textContent = originalText;

            if (placeholderContent) {
                placeholderContent.classList.remove('hidden');
            }
        }

    } catch (error) {
        injectionTarget.innerHTML = `<p style="color:red;">Error connecting to agent: ${error.message}</p>`;
        placeholderContent.textContent = originalText;

        if (placeholderContent) {
            placeholderContent.classList.remove('hidden');
        }
    }
});