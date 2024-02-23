document.addEventListener('DOMContentLoaded', async function () {
    const WEBSOCKET_URL = "ws://localhost:8000";
    const API_URL = "http://localhost:5000";
    const recordButton = document.getElementById('startRecordingButton');
    const stopButton = document.getElementById('stopRecordingButton');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messageForm = document.querySelector('#messageForm');
    const messageContainer = document.getElementById("messageContainer");
    const userContainer = document.getElementById("userContainer");
    let mediaRecorder;
    let recordedChunks = [];
    let clients = {};
    let targetConnectionID;
    let targetGroupID;
    let userID;
    
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    sendButton.addEventListener('click', sendMessage);
    messageForm.addEventListener('submit', sendMessage);

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function (event) {
            recordedChunks.push(event.data);
        };
        mediaRecorder.onstop = async function () {
            const audioBlob = new Blob(recordedChunks, { type: 'audio/mp3' });
            const formData = new FormData();
            formData.append('file', audioBlob);
            formData.append('type', "audio");
            try {
                const data = await uploadFile(formData, `${API_URL}/api/uploads/${targetGroupID}`);
                sendAudioData(data);
            } catch (error) {
                console.error("Error uploading audio:", error);
            }
        };
        mediaRecorder.start();
        recordButton.disabled = true;
        stopButton.disabled = false;
    }

    function stopRecording() {
        mediaRecorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    }

    async function sendMessage(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message !== "") {
            try {
                const userData = await authorizedFetch("/auth/me");
                if (userData.error) {
                    console.error("Error fetching user details:", userData.error);
                    return;
                }
                clients[targetConnectionID].send(JSON.stringify({
                    data: message,
                    type: "text",
                    user: userData
                }));
                messageInput.value = '';
                messageContainer.scrollTop = messageContainer.scrollHeight - messageContainer.clientHeight;
            } catch (error) {
                console.error("Error sending message:", error);
            }
        }
    }

    async function fetchUsers() {
        try {
            const responseData = await authorizedFetch("/api/users");
            if (responseData.hasOwnProperty('data')) {
                const users = responseData.data;
                users.forEach(user => {
                    const userCard = document.createElement("div");
                    userCard.classList.add("user-card");
                    userCard.innerHTML = `
                        <img src="${user.avatar}" alt="${user.username}" class="user-avatar">
                        <div class="user-details">
                            <h3 class="user-name">${user.username}</h3>
                            <p class="user-email">${user.email}</p>
                        </div>
                    `;
                    userCard.addEventListener('click', () => handleUserClick(user.username));
                    userContainer.appendChild(userCard);
                });
            } else {
                console.error("Error fetching users: Response does not contain 'data' field");
            }
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    }

    async function fetchMessages(groupID) {
        try {
            const data = await authorizedFetch(`/api/messages/${groupID}`);
            messageContainer.innerHTML = '';
            for (const row of data.data) {
                const textElement = document.createElement("p");
                const textNode = document.createTextNode(`${row.user.username}: ${row.message}`);
                textElement.setAttribute("class", "message");
                textElement.appendChild(textNode);
                messageContainer.appendChild(textElement);
                const lineBreak = document.createElement("br");
                messageContainer.appendChild(lineBreak);
            }
            messageContainer.scrollTop = messageContainer.scrollHeight;
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    }

    function handleUserClick(username) {
        console.log("Clicked on user:", username);
    }

    function sendAudioData(data) {
        if (targetConnectionID) {
            clients[targetConnectionID].send(JSON.stringify(data));
        }
    }

    async function authorizedFetch(endpoint) {
        const token = localStorage.getItem("token");
        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
        const response = await fetch(`${API_URL}${endpoint}`, { headers });
        return await response.json();
    }

    async function uploadFile(formData, url) {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }

    async function getGroupsHandler() {
        try {
            const userData = await authorizedFetch("/auth/me");
            userID = userData.id;
            sessionStorage.setItem("userID", userID);
            sessionStorage.setItem("username", userData.username);

            const data = await authorizedFetch("/api/groups");
            const groups = data.groups;
            for (let i = 0; i < groups.length; i++) {
                const group = groups[i];
                const connection = new WebSocket(`${WEBSOCKET_URL}/chat/${userID}/${group}`);
                clients[i] = connection;
                const perLink = document.createElement("li");
                const element = document.createElement("a");
                element.href = `javascript:void(0);`;
                element.textContent = group;
                element.addEventListener('click', () => {
                    messageContainer.innerHTML = '';
                    fetchMessages(group);
                    targetConnectionID = i;
                    targetGroupID = group;
                });
                perLink.appendChild(element);
                fetchGroups.appendChild(perLink);
                connection.onmessage = function (event) {
                    const messageData = JSON.parse(event.data);
                    if (messageData.type === 'text') {
                        const newMessage = document.createElement('p');
                        newMessage.setAttribute('class', 'message');
                        newMessage.textContent = `${messageData.user.username}: ${messageData.data}`;
                        const lineBreak = document.createElement("br");
                        messageContainer.appendChild(newMessage);
                        messageContainer.appendChild(lineBreak);
                    } else if (messageData.type === 'audio') {
                        const audioElement = document.createElement('audio');
                        audioElement.setAttribute('controls', 'controls');
                        audioElement.src = `${API_URL}/api/media/audio/${group}/${userID}`;
                        messageContainer.appendChild(audioElement);
                    }
                };
                connection.onclose = function () {
                    clients[i].close();
                };
            }
        } catch (error) {
            console.error("Error getting groups:", error);
        }
    }

    window.onload = () => {
        getGroupsHandler();
        fetchUsers();
    };

    window.onbeforeunload = () => {
        Object.values(clients).forEach(connection => connection.close());
    };
});
