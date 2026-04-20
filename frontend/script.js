const API_BASE = "/api";
let matchEnded = false;

// 1. Dynamic Match Data Binding
const matchDataDict = {
    "IPL2026-SRH-RCB-0522": {
        liveTeams: "SRH Batting",
        liveScore: "145/2",
        liveOvers: "14.2",
        finalString: "FINAL: SRH wins by 12 runs"
    },
    "IPL2026-CSK-MI-0524": {
        liveTeams: "CSK Batting",
        liveScore: "110/3",
        liveOvers: "12.0",
        finalString: "FINAL: CSK wins by 8 wickets"
    }
};

const matchSelector = document.getElementById("match-selector");
function updateMatchDisplay() {
    const selectedEvent = matchSelector.value;
    const data = matchDataDict[selectedEvent];
    const statusEl = document.getElementById("match-status");
    const mTeams = document.getElementById("match-teams");
    const mScore = document.getElementById("match-score");
    const mOvers = document.getElementById("match-overs");

    if (matchEnded) {
        statusEl.innerText = "MATCH ENDED";
        statusEl.className = "status-indicator ended";
        mTeams.innerText = data.finalString;
        mScore.innerText = "";
        mOvers.innerText = "";
    } else {
        statusEl.innerText = "LIVE";
        statusEl.className = "status-indicator live";
        mTeams.innerText = data.liveTeams;
        mScore.innerText = data.liveScore;
        mOvers.innerText = `(${data.liveOvers} ov)`;
    }
}
matchSelector.addEventListener("change", updateMatchDisplay);
updateMatchDisplay();


// Post-Match Toggle
document.getElementById("toggle-exit-mode").addEventListener("click", () => {
    matchEnded = !matchEnded;
    
    const uiBtn = document.getElementById("toggle-exit-mode");
    const off1T = document.getElementById("offer1-title");
    const off1D = document.getElementById("offer1-desc");
    const off2T = document.getElementById("offer2-title");
    const off2D = document.getElementById("offer2-desc");
    
    if(matchEnded) {
        uiBtn.innerText = "Reset Match";
        uiBtn.style.background = "#ef4444";
        uiBtn.style.color = "white";
        
        document.getElementById("gamification-card").style.display = "none";
        document.getElementById("safe-exit-card").style.display = "block";
        document.getElementById("tab-gates-lbl").innerText = "Exit Gates";
        
        off1T.innerText = "Stay Back & Eat";
        off1D.innerText = "50% off Food Court";
        off2T.innerText = "Travel Discount";
        off2D.innerText = "15% off Uber/Rapido Bookings";
    } else {
        uiBtn.innerText = "Simulate Match End";
        uiBtn.style.background = "rgba(255,255,255,0.1)";
        uiBtn.style.color = "white";
        
        document.getElementById("gamification-card").style.display = "block";
        document.getElementById("safe-exit-card").style.display = "none";
        document.getElementById("tab-gates-lbl").innerText = "Entry Gates";
        
        off1T.innerText = "Fast-Track Entry";
        off1D.innerText = "Gold Tier Exclusive";
        off2T.innerText = "Merch Discount";
        off2D.innerText = "20% Off Jerseys";
    }
    updateMatchDisplay();
    loadGates();
    if(typeof loadStaticTabs === "function") loadStaticTabs();
});


let tossMins = 124;
setInterval(() => {
    tossMins = tossMins > 0 ? tossMins - 1 : 0;
    document.getElementById("toss-countdown").innerText = tossMins;
}, 60000);

const tabBtns = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        tabBtns.forEach(b => b.classList.remove("active"));
        tabContents.forEach(c => c.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById(btn.dataset.target).classList.add("active");
    });
});

function renderHeatmapItems(containerId, items) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";
    items.forEach(item => {
        let colorCls = "val-low";
        let waitTime = "5 Mins";
        let subtitle = "";
        
        if(typeof item.density === 'number') {
             // Derive time from percentage (e.g. 1% = 0.3 mins roughly)
             let mins = Math.floor(item.density * 0.3);
             if(mins === 0) mins = 1;

             waitTime = `${mins} Mins`;
             subtitle = `${item.density}% Density`;
             
             if(item.density >= 70) colorCls = "val-high";
             else if(item.density >= 40) colorCls = "val-med";
        } else {
             // For explicit string values passed directly
             waitTime = item.density; 
             subtitle = "Est. Wait";
             if(item.density.includes("15") || item.density.includes("12")) colorCls = "val-high";
             else if(item.density.includes("5") || item.density.includes("10")) colorCls = "val-med";
        }

        const div = document.createElement("div");
        div.className = "heatmap-item";
        div.innerHTML = `
            <span class="heat-title">${item.name}</span>
            <span class="heat-val ${colorCls}">${waitTime}</span>
            <span class="heat-percent">${subtitle}</span>
        `;
        container.appendChild(div);
    });
}

async function loadGates() {
    try {
        const res = await fetch(`${API_BASE}/telemetry/wait-times`);
        const data = await res.json();
        const items = data.map(g => {
            if (matchEnded) {
                return { name: g.gate_name.replace('Gate', 'Exit'), density: Math.floor(Math.random() * 50 + 50) };
            }
            return { name: g.gate_name, density: g.density_percentage };
        });
        renderHeatmapItems("gates", items);
    } catch (e) {
        console.error("Gates map failed", e);
    }
}
setInterval(loadGates, 4000);
loadGates();

function loadStaticTabs() {
    if(matchEnded) {
        renderHeatmapItems("food", [
             {name: "Biryani Kiosk 1", density: "2 Mins"},
             {name: "Beverage Stand B", density: "0 Mins"},
        ]);
        renderHeatmapItems("restrooms", [
             {name: "East Wing", density: "2 Mins"}
        ]);
        return;
    }
    renderHeatmapItems("food", [
        {name: "Biryani Kiosk 1", density: "15 Mins"}, 
        {name: "Beverage Stand B", density: "2 Mins"}, 
        {name: "Burger Spot", density: "5 Mins"}
    ]);
    renderHeatmapItems("restrooms", [
        {name: "East Wing", density: "10 Mins"}, 
        {name: "West Wing", density: "3 Mins"}, 
        {name: "North Gate", density: "12 Mins"}
    ]);
}

setInterval(loadStaticTabs, 4000);
loadStaticTabs();

const chatMessages = [
    { role: "user", content: "My friend is feeling dizzy and the crowd here is too tight to move" },
    { role: "assistant", content: "I am dispatching a medical response team to your exact location in the South Terrace right now. Please stay exactly where you are. A stadium steward wearing a bright orange vest has been notified and is approaching your section to assist you immediately." },
    { role: "user", content: "Okay, I see them. Thank you." },
    { role: "assistant", content: "You're welcome. VenueScout is standing by if you need anything else." }
];

const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-input");
const btnSend = document.getElementById("send-btn");
const toggleBtn = document.getElementById("toggle-chat");
const chatHeaderObj = document.getElementById("chat-header");
const notificationBadge = document.getElementById("notif-badge");

function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
}

function appendMessage(role, htmlContent) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.innerHTML = htmlContent;
    chatBody.appendChild(div);
    scrollToBottom();
    return div;
}

function renderChatInitial() {
    chatBody.innerHTML = "";
    chatMessages.forEach(m => appendMessage(m.role, m.content));
}
renderChatInitial();

async function handleSend() {
    const text = chatInput.value.trim();
    if(!text) return;
    
    chatMessages.push({ role: "user", content: text });
    appendMessage("user", text);
    chatInput.value = "";

    const typingBubble = appendMessage("assistant", '<div class="typing-indicator"><span></span><span></span><span></span></div>');

    try {
        const res = await fetch(`${API_BASE}/ai/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages: chatMessages })
        });
        const data = await res.json();
        
        typingBubble.remove();
        chatMessages.push({ role: "assistant", content: data.reply });
        appendMessage("assistant", data.reply.replace(/\n/g, "<br>"));
    } catch (e) {
        typingBubble.remove();
        appendMessage("assistant", "VenueScout is currently offline connecting to the mainframe.");
    }
}

btnSend.addEventListener("click", handleSend);
chatInput.addEventListener("keypress", (e) => {
    if(e.key === "Enter") handleSend();
});

let chatOpen = false;
chatHeaderObj.addEventListener("click", () => {
    chatOpen = !chatOpen;
    // Dismiss proactive badge on click
    if(notificationBadge) notificationBadge.style.display = "none"; 
    
    if(chatOpen) {
        document.getElementById("chat-body").classList.remove("collapsed");
        document.querySelector(".chat-footer").classList.remove("collapsed");
        toggleBtn.innerText = "▼";
        scrollToBottom();
    } else {
        document.getElementById("chat-body").classList.add("collapsed");
        document.querySelector(".chat-footer").classList.add("collapsed");
        toggleBtn.innerText = "▲";
    }
});


const sosBtn = document.getElementById("sos-btn");
const sosModal = document.getElementById("sos-modal");
const closeModal = document.getElementById("close-modal");
const sosForm = document.getElementById("sos-form");
const toast = document.getElementById("toast");

sosBtn.addEventListener("click", () => sosModal.classList.add("active"));
closeModal.addEventListener("click", () => sosModal.classList.remove("active"));

sosForm.addEventListener("submit", (e) => {
    e.preventDefault(); 
    sosModal.classList.remove("active");
    sosForm.reset();
    
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 4000);
});

document.querySelectorAll('.claim-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.innerText = "Claimed!";
        btn.style.background = "var(--green)";
        btn.style.cursor = "default";
    });
});
