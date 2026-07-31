// ==========================================================
// CREATOR COMPASS CHAT
// ==========================================================

// ==========================================================
// DOM ELEMENTS
// ==========================================================

const form = document.getElementById("chatForm");
const input = document.getElementById("message");
const workspaceBody = document.getElementById("workspaceBody");
const sendButton = document.getElementById("sendButton");
const timeline = document.getElementById("timeline");

const analyzeButton = document.getElementById("analyzeButton");
const creatorScore = document.getElementById("creatorScore");
const creatorDashboardMessage = document.getElementById("creatorDashboardMessage");

let isSending = false;

// ==========================================================
// INITIAL SCROLL
// ==========================================================
if (
    workspaceBody
) {
    scrollToBottom();
}

// ==========================================================
// SCROLL
// ==========================================================

function scrollToBottom() {

    workspaceBody.scrollTop = workspaceBody.scrollHeight;

}

// ==========================================================
// ESCAPE HTML
// ==========================================================

function escapeHTML(text) {

    const div = document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}

// ==========================================================
// CREATE MESSAGE
// ==========================================================

function createMessage(role, sender, text) {

    const message = document.createElement("div");

    message.className = `${role}-message`;

    message.innerHTML = `

        <strong>${sender}</strong>

        <p>${escapeHTML(text)}</p>

    `;

    workspaceBody.appendChild(message);

    scrollToBottom();

}

// ==========================================================
// UPDATE TIMELINE
// ==========================================================

function updateTimeline(items = []) {

    if (!timeline) return;

    timeline.innerHTML = "";

    if (items.length === 0) {

        timeline.innerHTML = `

            <p class="timeline-empty">

                No previous conversations.

            </p>

        `;

        return;

    }

    items.forEach(item => {

        const div = document.createElement("div");

        div.className = "timeline-item";

        div.dataset.id = item.id;

        div.innerHTML = `

            <div class="timeline-time">

                ${item.time}

            </div>

            <div class="timeline-title">

                ${escapeHTML(item.title)}

            </div>

        `;

        timeline.appendChild(div);

    });

}

// ==========================================================
// TYPING
// ==========================================================

function showTyping() {

    removeTyping();

    const typing = document.createElement("div");

    typing.id = "typingIndicator";

    typing.className = "assistant-message";

    typing.innerHTML = `

        <strong>Creator Compass</strong>

        <div class="typing">

            <span></span>

            <span></span>

            <span></span>

        </div>

    `;

    workspaceBody.appendChild(typing);

    scrollToBottom();

}

function removeTyping() {

    const typing = document.getElementById("typingIndicator");

    if (typing) {

        typing.remove();

    }

}

// ==========================================================
// SEND MESSAGE
// ==========================================================

async function sendMessage(event) {

    event.preventDefault();

    if (isSending) return;

    const message = input.value.trim();

    if (!message) return;

    isSending = true;

    sendButton.disabled = true;

    createMessage(

        "user",

        "You",

        message

    );

    input.value = "";

    showTyping();

    try {

        const response = await fetch(

            "/send_message",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    message: message

                })

            }

        );

        const data = await response.json();

        removeTyping();

        createMessage(

            "assistant",

            "Creator Compass",

            data.assistant

        );

        updateTimeline(

            data.timeline

        );

    }

    catch(error){

        removeTyping();

        createMessage(

            "assistant",

            "Creator Compass",

            "Unable to connect to Creator Compass."

        );

        console.error(error);

    }

    finally{

        sendButton.disabled = false;

        isSending = false;

        input.focus();

    }

}
// ==========================================================
// ANALYZE
// ==========================================================

async function analyzeContent() {

    if (!creatorScore) return;

    const messages = workspaceBody.querySelectorAll(".user-message");

    if (messages.length === 0) {

        creatorScore.textContent = "-- / 100";

        creatorDashboardMessage.textContent =
            "Send a message before analyzing.";

        return;

    }

    const latest = messages[messages.length - 1]
        .querySelector("p")
        .innerText;

    analyzeButton.disabled = true;

    analyzeButton.textContent = "Analyzing...";

    try {

        const response = await fetch(

            "/analyze_content",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    content: latest

                })

            }

        );

        if (!response.ok) {

            throw new Error("Failed to analyze content.");

        }

        const data = await response.json();

        const dashboard = data.dashboard;

        creatorScore.innerHTML = `

            <div style="font-size:32px;font-weight:bold;">

                ${dashboard.overall} / 100

            </div>

            <div class="dashboard-rating">

                ${dashboard.rating}

            </div>

        `;

        creatorDashboardMessage.innerHTML = `

            <b>Title Strength</b> : ${dashboard.title}/20
            <br><br>

            <b>Hook</b> : ${dashboard.hook}/20
            <br><br>

            <b>SEO</b> : ${dashboard.seo}/20
            <br><br>

            <b>Creativity</b> : ${dashboard.creativity}/20
            <br><br>

            <b>Audience Appeal</b> : ${dashboard.audience}/20

            <hr>

            <b>Strengths</b>

            <ul>

                ${dashboard.strengths
                    .map(item => `<li>${item}</li>`)
                    .join("")}

            </ul>

            <b>Suggestions</b>

            <ul>

                ${dashboard.suggestions
                    .map(item => `<li>${item}</li>`)
                    .join("")}

            </ul>

        `;

    }

    catch(error){

        console.error(error);

        creatorScore.textContent = "-- / 100";

        creatorDashboardMessage.textContent =
            "Unable to analyze content.";

    }

    finally{

        analyzeButton.disabled = false;

        analyzeButton.textContent = "Analyze";

    }

}
// ==========================================================
// EVENTS
// ==========================================================

form.addEventListener(

    "submit",

    sendMessage

);

input.addEventListener(

    "keydown",

    function(event){

        if(event.key==="Enter"){

            event.preventDefault();

            form.requestSubmit();

        }

    }

);

if(analyzeButton){

    analyzeButton.addEventListener(

        "click",

        analyzeContent

    );

}