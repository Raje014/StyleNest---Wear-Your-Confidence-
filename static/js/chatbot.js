const chatToggle = document.getElementById("chat-toggle");
const chatWindow = document.getElementById("chat-window");
const chatClose = document.getElementById("chat-close");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-message");
const chatMessages = document.getElementById("chat-messages");

chatToggle.addEventListener("click", () => {
    chatWindow.style.display = "flex";
    chatToggle.style.display = "none";
    chatInput.focus();
});

chatClose.addEventListener("click", () => {
    chatWindow.style.display = "none";
    chatToggle.style.display = "block";
});

function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );
    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    contentDiv.innerHTML = marked.parse(message);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    addMessage(message, "user");
    chatInput.value = "";
    // Loading message
    const loadingDiv = document.createElement("div");
    loadingDiv.classList.add(
        "message",
        "bot-message"
    );
    loadingDiv.innerHTML = `
        <div class="message-content">
            Thinking... ✨
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
    try {
        const csrftoken = getCookie("csrftoken");
        const response = await fetch("/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                message: message
            })
        });
        const data = await response.json();
        loadingDiv.remove();
        if (data.success) {
            addMessage(
                data.response,
                "bot"
            );
        } else {
            addMessage(
                "Sorry, something went wrong.",
                "bot"
            );
            console.error(data.error);
        }
    } catch (error) {
        loadingDiv.remove();
        addMessage(
            "Unable to connect to the AI assistant.",
            "bot"
        );
        console.error(error);
    }
}

sendButton.addEventListener(
    "click",
    sendMessage
);

chatInput.addEventListener(
    "keypress",
    (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
);