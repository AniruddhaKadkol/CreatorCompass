// DOM ELEMENTS

const form = document.getElementById("storyForm");
const input = document.getElementById("storyMessage");
const workspaceBody = document.getElementById("workspaceBody");
const sendButton = document.getElementById("storySendButton");
const timeline = document.getElementById("storyTimeline");
const analyzeButton = document.getElementById("storyAnalyzeButton");
const score = document.getElementById("storyScore");
const dashboard = document.getElementById("storyDashboardMessage");

let sending = false;
// INITIAL SCROLL

if (workspaceBody) {
    scrollBottom();
}
// SCROLL

function scrollBottom() {
    workspaceBody.scrollTop = workspaceBody.scrollHeight;
}
// ESCAPE HTML

function escapeHTML(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}
// CREATE MESSAGE

function addMessage(role, sender, text) {
    const message = document.createElement("div");
    message.className = `${role}-message`;
    message.innerHTML = `
        <strong>${sender}</strong>
        <p>${escapeHTML(text)}</p>
    `;
    workspaceBody.appendChild(message);
    scrollBottom();
}
// UPDATE TIMELINE

function updateTimeline(items = []) {
    if (!timeline) return;
    timeline.innerHTML = "";
    if (items.length === 0) {
        timeline.innerHTML = `
            <p class="timeline-empty">
                No previous creative sessions.
            </p>
        `;
        return;
    }
    items.forEach(item => {
        const div = document.createElement("div");
        div.className = "timeline-item";
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
// TYPING INDICATOR

function showTyping() {
    removeTyping();
    const div = document.createElement("div");
    div.id = "typingIndicator";
    div.className = "assistant-message";
    div.innerHTML = `
        <strong>
            Creator Compass
        </strong>
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    workspaceBody.appendChild(div);
    scrollBottom();
}
function removeTyping() {
    const typing = document.getElementById("typingIndicator");
    if (typing) {
        typing.remove();
    }
}
// SEND CREATIVE MESSAGE

async function sendCreativeMessage(event) {
    event.preventDefault();
    if (sending) return;
    const message = input.value.trim();
    if (!message) return;
    sending = true;
    sendButton.disabled = true;
    addMessage(
       "user",
        "You",
        message
    );
    input.value = "";
    showTyping();
    try {
        const response = await fetch(
            "/send_creative_message",
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
        if (!data.success) {
            addMessage(
                "assistant",
                "Creator Compass",
                data.error || "Something went wrong."
            );
        }
        else {
            addMessage(
                "assistant",
                "Creator Compass",
                 data.assistant
            );
            updateTimeline(
                data.timeline || []
            );
        }
    }
    catch (error) {
        console.error(error);
        removeTyping();
        addMessage(
            "assistant",
            "Creator Compass",
            "Unable to connect to Creator Compass."
        );
    }
    finally {
        sending = false;
        sendButton.disabled = false;
        input.focus();
    }
}
// CREATOR DASHBOARD

async function analyzeCreativeProject() {
    const messages =
        workspaceBody.querySelectorAll(".user-message");
    if (messages.length === 0) {
        score.textContent = "-- / 100";
        dashboard.textContent =
            "Create something before analyzing.";
        return;
    }
    const latest =
        messages[messages.length - 1]
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
        const data = await response.json();
        const d = data.dashboard;
        score.textContent =
            `${d.overall} / 100`;
        dashboard.innerHTML = `
<b>Overall Rating</b><br>
${d.rating}<br><br>
<b>Title Strength</b>: ${d.title}/20<br>
<b>Hook</b>: ${d.hook}/20<br>
<b>SEO</b>: ${d.seo}/20<br>
<b>Creativity</b>: ${d.creativity}/20<br>
<b>Audience Appeal</b>: ${d.audience}/20<br><br>
<b>Strengths</b><br>
${d.strengths.join("<br>")}<br><br>
<b>Suggestions</b><br>
${d.suggestions.join("<br>")}
`;
    }
    catch (error) {
        console.error(error);
        dashboard.textContent =
            "Unable to analyze your creative project.";
    }
    finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze";
    }
}
// EVENTS

form.addEventListener(
    "submit",
    sendCreativeMessage
);
input.addEventListener(
    "keydown",
    function(event){
        if(event.key === "Enter"){
            event.preventDefault();
            form.requestSubmit();
        }
    }
);
if(analyzeButton){
    analyzeButton.addEventListener(
        "click",
        analyzeCreativeProject
    );
}