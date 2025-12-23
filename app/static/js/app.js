/**
 * app.js: JS code for the adk-sample app.
 */

/**
 * HTTP Request handling
 */

// Generate or retrieve session ID for persistent memory
function getSessionId() {
  let sessionId = sessionStorage.getItem('chat_session_id');
  if (!sessionId) {
    sessionId = 'session_' + Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem('chat_session_id', sessionId);
  }
  return sessionId;
}

const SESSION_ID = getSessionId();
console.log('[SESSION] Using session ID:', SESSION_ID);

// Get DOM elements
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("message");
const messagesDiv = document.getElementById("messages");
const typingIndicator = document.getElementById("typing-indicator");

// Initialize - enable send button
document.getElementById("sendButton").disabled = false;


// --- Chat history persistence ---
const CHAT_STORAGE_KEY = 'adk_chat_history';
function saveChatHistory(history) {
  localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(history));
}
function loadChatHistory() {
  try {
    return JSON.parse(localStorage.getItem(CHAT_STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}
function addMessageToHistory(role, text) {
  const history = loadChatHistory();
  history.push({ role, text });
  saveChatHistory(history);
}
function clearChatHistory() {
  localStorage.removeItem(CHAT_STORAGE_KEY);
}
function renderChatHistory() {
  // Preserve typing indicator and scroll indicator, clear only messages
  const existingMessages = messagesDiv.querySelectorAll('.user-message, .agent-message');
  existingMessages.forEach(msg => msg.remove());

  const history = loadChatHistory();
  const typingInd = document.getElementById('typing-indicator');

  for (const msg of history) {
    const p = document.createElement('p');
    p.textContent = msg.text;
    if (msg.role === 'user') p.className = 'user-message';
    else p.className = 'agent-message';
    // Insert before typing indicator
    if (typingInd) {
      messagesDiv.insertBefore(p, typingInd);
    } else {
      messagesDiv.appendChild(p);
    }
  }

  // Activate chat if there's history
  if (history.length > 0) {
    document.body.classList.add('chat-active');
  }

  // Always scroll to bottom after rendering
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Render chat history on page load
renderChatHistory();

// Add submit handler to the form
messageForm.onsubmit = async function (e) {
  e.preventDefault();
  const message = messageInput.value;
  if (message) {
    // Ensure chat is visible and show user message
    document.body.classList.add('chat-active');

    // Display user message
    const userMessageElem = document.createElement("p");
    userMessageElem.textContent = message;
    userMessageElem.className = "user-message";
    messagesDiv.appendChild(userMessageElem);
    addMessageToHistory('user', message);
    messageInput.value = "";

    // Show typing indicator (use global function if available, fallback to direct)
    if (window.showTypingIndicator) {
      window.showTypingIndicator();
    } else {
      typingIndicator.classList.add("visible");
    }
    console.log("[CLIENT TO AGENT] " + message);

    try {
      // Send message to server with session ID for memory
      const response = await fetch("/api/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          session_id: SESSION_ID,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("[AGENT TO CLIENT] ", data);

      // Hide typing indicator
      if (window.hideTypingIndicator) {
        window.hideTypingIndicator();
      } else {
        typingIndicator.classList.remove("visible");
      }

      // Display agent response
      const agentMessageElem = document.createElement("p");
      agentMessageElem.textContent = data.response || data.message || "No response";
      agentMessageElem.className = "agent-message";
      messagesDiv.appendChild(agentMessageElem);
      addMessageToHistory('agent', agentMessageElem.textContent);
    } catch (error) {
      console.error("Error sending message:", error);
      if (window.hideTypingIndicator) {
        window.hideTypingIndicator();
      } else {
        typingIndicator.classList.remove("visible");
      }
      const errorMessageElem = document.createElement("p");
      errorMessageElem.textContent = "Error: Could not send message";
      errorMessageElem.className = "agent-message";
      messagesDiv.appendChild(errorMessageElem);
      addMessageToHistory('agent', errorMessageElem.textContent);
    }

    // Scroll to the bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  return false;
};


