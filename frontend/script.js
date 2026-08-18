const API_URL = "http://127.0.0.1:8000";

const questionInput = document.getElementById("question");
const chat = document.getElementById("chat");
const sendButton = document.getElementById("sendButton");


function useSuggestion(text) {

    questionInput.value = text;

    questionInput.focus();
}


function handleKey(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        askQuestion();
    }
}


function addUserMessage(question) {

    const message = document.createElement("div");

    message.className = "message user-message";

    message.innerHTML = `
        <div class="user-bubble">
            ${escapeHtml(question)}
        </div>
    `;

    chat.appendChild(message);

    scrollToBottom();
}


function addLoadingMessage() {

    const message = document.createElement("div");

    message.className = "message ai-message";

    message.id = "loading-message";

    message.innerHTML = `
        <div class="ai-icon">✦</div>

        <div class="ai-content">

            <div class="loading">
                <span></span>
                <span></span>
                <span></span>
            </div>

        </div>
    `;

    chat.appendChild(message);

    scrollToBottom();
}


function removeLoadingMessage() {

    const loading = document.getElementById("loading-message");

    if (loading) {
        loading.remove();
    }
}


function addAIMessage(data) {

    const message = document.createElement("div");

    message.className = "message ai-message";

    let sourcesHTML = "";

    if (data.sources && data.sources.length > 0) {

        sourcesHTML = `
            <div class="sources">

                <div class="sources-title">
                    Sources
                </div>

                ${data.sources.map(source => `
                    <div class="source">
                        📄
                        <span>
                            ${escapeHtml(source.document || "Document")}
                            ${source.page ? ` — Page ${escapeHtml(source.page)}` : ""}
                        </span>
                    </div>
                `).join("")}

            </div>
        `;
    }


    message.innerHTML = `
        <div class="ai-icon">✦</div>

        <div class="ai-content">

            <div>
                ${escapeHtml(data.answer)}
            </div>

            ${sourcesHTML}

        </div>
    `;

    chat.appendChild(message);

    scrollToBottom();
}


async function askQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }


    addUserMessage(question);

    questionInput.value = "";

    sendButton.disabled = true;

    addLoadingMessage();


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data = await response.json();


        removeLoadingMessage();

        addAIMessage(data);


    } catch (error) {

        removeLoadingMessage();

        addAIMessage({
            answer:
                "Unable to connect to the Chitkara RAG backend. Make sure the FastAPI server is running.",
            sources: []
        });

        console.error(error);

    } finally {

        sendButton.disabled = false;

        questionInput.focus();
    }
}


function scrollToBottom() {

    chat.scrollTo({
        top: chat.scrollHeight,
        behavior: "smooth"
    });
}


function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}