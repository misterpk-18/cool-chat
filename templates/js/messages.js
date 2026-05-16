const BASE_URL = "http://127.0.0.1:5000";

let currentUser = null;
let currentConversationId = null;
let isGroup = false;
let chatType = "dm";
let typingTimeout = null;
let socket = null;


// ─── INIT ───────────────────────────────────────────────

window.onload = function () {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        window.location.href = "login.html";
        return;
    }
    currentUser = user;
    document.getElementById("welcomeText").textContent = `Hi, ${user.username}`;
    initSocket();
    loadConversations();
};


// ─── SOCKET.IO ──────────────────────────────────────────

function initSocket() {
    socket = io(BASE_URL);

    socket.on("connect", () => {
        console.log("Socket connected");
    });

    socket.on("new_message", (data) => {
        if (data.conversation_id == currentConversationId) {
            appendMessage(data, data.sender_id === currentUser.userid);
            scrollToBottom();
            // Mark as seen
            socket.emit("message_seen", {
                conversation_id: currentConversationId,
                user_id: currentUser.userid
            });
        }
        // Update conversation preview
        updateConvoPreview(data.conversation_id, data.content);
    });

    socket.on("user_typing", (data) => {
        document.getElementById("typingIndicator").style.display = "block";
        document.getElementById("typingText").textContent = `${data.username} is typing...`;
    });

    socket.on("user_stop_typing", () => {
        document.getElementById("typingIndicator").style.display = "none";
        document.getElementById("typingText").textContent = "";
    });

    socket.on("seen_update", () => {
        // could add seen ticks here in future
    });
}


// ─── CONVERSATIONS ──────────────────────────────────────

async function loadConversations() {
    const res = await fetch(`${BASE_URL}/conversations/${currentUser.userid}`);
    const data = await res.json();
    const list = document.getElementById("conversationsList");

    if (!data.conversations || data.conversations.length === 0) {
        list.innerHTML = `<div class="empty-state">No conversations yet</div>`;
        return;
    }

    list.innerHTML = "";

    for (const convo of data.conversations) {
        await renderConversationItem(convo);
    }
}

async function renderConversationItem(convo) {
    const list = document.getElementById("conversationsList");

    let name = convo.is_group ? (convo.group_name || "Group Chat") : "";

    // For DMs fetch the other person's username before rendering
    if (!convo.is_group) {
        const res = await fetch(`${BASE_URL}/conversations/${convo.id}/members`);
        const data = await res.json();
        const other = data.members.find(m => m.userid !== currentUser.userid);
        name = other ? other.username : "Unknown";
    }

    const initial = name.charAt(0).toUpperCase();

    const item = document.createElement("div");
    item.className = "conversation-item";
    item.id = `convo-${convo.id}`;
    item.onclick = () => openConversation(convo.id, name, convo.is_group);
    item.innerHTML = `
        <div class="convo-avatar">${initial}</div>
        <div class="convo-info">
            <div class="convo-name" id="convo-name-${convo.id}">${name}</div>
            <div class="convo-preview" id="preview-${convo.id}">Tap to open</div>
        </div>
    `;
    list.appendChild(item);
}

function updateConvoPreview(conversation_id, content) {
    const preview = document.getElementById(`preview-${conversation_id}`);
    if (preview) {
        preview.textContent = content.length > 40 ? content.substring(0, 40) + "..." : content;
    }
}


// ─── OPEN CONVERSATION ──────────────────────────────────

async function openConversation(conversationId, name, isGroupChat) {
    // Leave previous room
    if (currentConversationId) {
        socket.emit("leave_conversation", {
            conversation_id: currentConversationId,
            user_id: currentUser.userid
        });
    }

    currentConversationId = conversationId;
    isGroup = isGroupChat;

    // Update active state
    document.querySelectorAll(".conversation-item").forEach(el => el.classList.remove("active"));
    const activeItem = document.getElementById(`convo-${conversationId}`);
    if (activeItem) activeItem.classList.add("active");

    // Show chat window
    document.getElementById("emptyChatState").style.display = "none";
    document.getElementById("chatWindow").style.display = "flex";
    document.getElementById("chatName").textContent = name;

    // Show add member button for groups
    document.getElementById("addMemberBtn").style.display = isGroupChat ? "block" : "none";

    // Load members
    await loadMembers(conversationId, isGroupChat);

    // Load messages
    await loadMessages(conversationId);

    // Join socket room
    socket.emit("join_conversation", {
        conversation_id: conversationId,
        user_id: currentUser.userid
    });
}

async function loadMembers(conversationId, isGroupChat) {
    const res = await fetch(`${BASE_URL}/conversations/${conversationId}/members`);
    const data = await res.json();

    if (isGroupChat) {
        const names = data.members.map(m => m.username).join(", ");
        document.getElementById("chatMembers").textContent = names;
        document.getElementById("chatName").textContent = data.members.find(m => m.userid !== currentUser.userid)?.username || "Group Chat";

        // Update conversation list item name
        const nameEl = document.getElementById(`convo-name-${conversationId}`);
        if (nameEl) nameEl.textContent = document.getElementById("chatName").textContent;

    } else {
        const other = data.members.find(m => m.userid !== currentUser.userid);
        if (other) {
            document.getElementById("chatName").textContent = other.username;

            // Update conversation list item name
            const nameEl = document.getElementById(`convo-name-${conversationId}`);
            if (nameEl) nameEl.textContent = other.username;
        }
        document.getElementById("chatMembers").textContent = "";
    }
}

async function loadMessages(conversationId) {
    const messagesArea = document.getElementById("messagesArea");
    messagesArea.innerHTML = "";

    const res = await fetch(`${BASE_URL}/conversations/${conversationId}/messages`);
    const data = await res.json();

    if (!data.messages || data.messages.length === 0) {
        messagesArea.innerHTML = `<div class="empty-state">No messages yet. Say hello! 👋</div>`;
        return;
    }

    data.messages.forEach(msg => {
        appendMessage(msg, msg.sender_id === currentUser.userid);
    });

    scrollToBottom();
}


// ─── MESSAGES ───────────────────────────────────────────

function appendMessage(msg, isSent) {
    const messagesArea = document.getElementById("messagesArea");

    // Remove empty state if present
    const emptyState = messagesArea.querySelector(".empty-state");
    if (emptyState) emptyState.remove();

    const wrap = document.createElement("div");
    wrap.className = `message-bubble-wrap ${isSent ? "sent" : "received"}`;

    const time = new Date(msg.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    wrap.innerHTML = `
        ${!isSent ? `<div class="message-sender-name">${msg.username || msg.sender_id}</div>` : ""}
        <div class="message-bubble">${msg.content}</div>
        ${msg.media_url ? `<img src="${msg.media_url}" class="message-image" />` : ""}
        <div class="message-time">${time}</div>
    `;

    messagesArea.appendChild(wrap);
}

function scrollToBottom() {
    const messagesArea = document.getElementById("messagesArea");
    messagesArea.scrollTop = messagesArea.scrollHeight;
}


// ─── SEND MESSAGE ────────────────────────────────────────

function sendMessage() {
    const input = document.getElementById("messageInput");
    const content = input.value.trim();

    if (!content || !currentConversationId) return;

    socket.emit("send_message", {
        conversation_id: currentConversationId,
        sender_id: currentUser.userid,
        content: content
    });

    input.value = "";
    input.style.height = "auto";

    // Stop typing indicator
    socket.emit("stop_typing", {
        conversation_id: currentConversationId,
        user_id: currentUser.userid
    });
}

function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function handleTyping() {
    if (!currentConversationId) return;

    // Auto resize textarea
    const input = document.getElementById("messageInput");
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";

    socket.emit("typing", {
        conversation_id: currentConversationId,
        user_id: currentUser.userid,
        username: currentUser.username
    });

    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        socket.emit("stop_typing", {
            conversation_id: currentConversationId,
            user_id: currentUser.userid
        });
    }, 1500);
}


// ─── CREATE CONVERSATION ─────────────────────────────────

function openNewChatModal() {
    document.getElementById("newChatModal").style.display = "flex";
    document.getElementById("modalMessage").textContent = "";
    document.getElementById("memberIdsInput").value = "";
    document.getElementById("groupNameInput").value = "";
    selectType("dm");
}

function closeNewChatModal() {
    document.getElementById("newChatModal").style.display = "none";
}

function selectType(type) {
    chatType = type;
    document.getElementById("dmBtn").classList.toggle("active", type === "dm");
    document.getElementById("groupBtn").classList.toggle("active", type === "group");
    document.getElementById("groupNameField").style.display = type === "group" ? "block" : "none";
}

async function createConversation() {
    const memberInput = document.getElementById("memberIdsInput").value.trim();
    const groupName = document.getElementById("groupNameInput").value.trim();
    const modalMessage = document.getElementById("modalMessage");

    if (!memberInput) {
        modalMessage.textContent = "Please enter at least one username.";
        return;
    }

    const enteredUsernames = memberInput.split(",").map(u => u.trim()).filter(Boolean);

    // Resolve usernames to userids
    modalMessage.textContent = "Looking up users...";
    modalMessage.style.color = "#999";

    const resolvedIds = [];
    for (const username of enteredUsernames) {
        const res = await fetch(`${BASE_URL}/search-users?q=${username}`);
        const data = await res.json();
        const match = data.users?.find(u => u.username.toLowerCase() === username.toLowerCase());
        if (!match) {
            modalMessage.textContent = `User "${username}" not found.`;
            modalMessage.style.color = "#e74c3c";
            return;
        }
        resolvedIds.push(match.userid);
    }

    const memberIds = [currentUser.userid, ...resolvedIds];

    if (chatType === "dm" && memberIds.length !== 2) {
        modalMessage.textContent = "DM requires exactly one other username.";
        modalMessage.style.color = "#e74c3c";
        return;
    }

    if (chatType === "group" && !groupName) {
        modalMessage.textContent = "Please enter a group name.";
        modalMessage.style.color = "#e74c3c";
        return;
    }

    const body = {
        is_group: chatType === "group",
        member_ids: memberIds,
        group_name: chatType === "group" ? groupName : null
    };

    const res = await fetch(`${BASE_URL}/conversations/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    if (res.ok) {
        closeNewChatModal();
        await loadConversations();
        const name = chatType === "group" ? groupName : ``;
        openConversation(data.conversation_id, name, chatType === "group");
    } else {
        modalMessage.textContent = data.error || "Something went wrong.";
        modalMessage.style.color = "#e74c3c";
    }
}

// ─── ADD MEMBER ──────────────────────────────────────────

function openAddMemberModal() {
    document.getElementById("addMemberModal").style.display = "flex";
    document.getElementById("addMemberInput").value = "";
    document.getElementById("addMemberMessage").textContent = "";
}

function closeAddMemberModal() {
    document.getElementById("addMemberModal").style.display = "none";
}

async function addMember() {
    const userId = document.getElementById("addMemberInput").value.trim();
    const msg = document.getElementById("addMemberMessage");

    if (!userId) {
        msg.textContent = "Please enter a user ID.";
        return;
    }

    const res = await fetch(`${BASE_URL}/conversations/add-member`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: currentConversationId, user_id: userId })
    });

    const data = await res.json();

    if (res.ok) {
        closeAddMemberModal();
        await loadMembers(currentConversationId, true);
    } else {
        msg.textContent = data.error || "Something went wrong.";
    }
}


// ─── NAVIGATION ──────────────────────────────────────────

function goToProfile() {
    window.location.href = `profile.html?userid=${currentUser.userid}`;
}

function goToHome() {
    window.location.href = "home.html";
}

function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}
