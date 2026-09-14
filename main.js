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

import { initNav, initSidebarToggle, getAppType } from 'modules/nav.js';
import * as auth from 'modules/auth.js';
import CONFIG from './config.js';


export async function getAgents(){
  try {
    
    const response = await fetch('ai-helper/models.json');

    if (!response.ok){
      throw new Error(`HTTP status: ${response.status}`);
      return;
    }

    console.log(response);

    return response;
   

  } catch (error) {
    console.error("Failed to fetch data from FastAPI:", error);
  }
}

export async function sendPrompt(message, chat_id, session_id){
  try {
    const payload = await fetch(CONFIG.FASTAPI_URL + "/api/chat/completions", {
      method: "POST",
      body: JSON.stringify(message)
    });

    if (!payload.ok) {
      throw new Error(`HTTP error! Status: ${payload.status}`);
    }

    const agentMessage = await payload.json();
    console.log("Successfully retrieved agent response:", response);

    return agentMessage;
    
  } catch (error) {
    console.error("Failed to fetch data from FastAPI:", error);
  }
}


// Main initialization function that sets up the sidebar toggle, loads the initial app view, and handles browser navigation events
async function init() {
   /*
  try {
    const authenticated = await auth.initAuth();

    if (authenticated) { 
      console.log("User succesfuly authenticated", authenticated.INSERTAUTHSTATUS);
    } else {
      throw error;
      return; 
    }

  } catch (error) {
    console.log(`Failed to authenticate user: ${authenticated.INSERTAUTHSTATUS}`);
  }
  */

  // Element definitions
  const appWrapper = document.getElementById('app-container');
  if (appWrapper) {
    appWrapper.classList.add('ready');
  } else {
    return;
  }

  const chatContainer = document.getElementById('chat-container');
  const chatInput = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  const injectionTarget = document.getElementById('app');
  const placeholderContent = document.querySelector('.placeholder-content');
  const originalText = placeholderContent.textContent;
  const placeholderContent_text = originalText;

  // Initialize sidebar toggle listener (nav.js) 
  // DELETE THIS ONCE MERGED TO NAV INIT
  initSidebarToggle();

  // await initNav();


  // Event listener for the generate button for chat
  sendBtn.addEventListener('click', async () => {
      const prompt = chatInput.value.trim(); // removes any unecessary whitespaces on beginning and end of user input
      if (!prompt) return;

      try {
        // Fetches the AI response from API
        const response = await sendPrompt();
        const codeRegex = /(function\s+\w+|.*?\s*=>|\b(const|let|var)\b|```[a-z]*\n|[\{\};])/g; // Regex definition for checkig if AI generated code

        // REVIEW!!!!

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

  // Listen for browser navigation events (back/forward) and reload the app view accordingly
  // Ensures the entire website is NOT reloaded and just the app view is
  window.addEventListener('popstate', () => {
    //navigation.loadAppView(navigation.getAppType());
  });
}

init();