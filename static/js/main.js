//Hämta kontinuerligt nya meddelanden från servern 
var socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on("new_disconnect", function(message) {
    // Någon loggade ut
    document.getElementById("messages").innerHTML += '<div class="message" id="highlight-disconnect"><span class="message-username">' + message + '</span></div>';
    updateScroll();
});
socket.on("new_connect", function(message) {
    // Någon anslöt
    document.getElementById("messages").innerHTML += '<div class="message" id="highlight-connect"><span class="message-username">' + message + '</span></div>';
    updateScroll();
});
socket.on("new_message", function(data) {
    // Lägg till dem nya meddelandena
    document.getElementById("messages").innerHTML += '<div class="message"><span class="message-username">' + data["username"] + ':</span><span class ="message-sent">' + data["message"] + '<span></div>';
    updateScroll();
});
socket.on("redirect", function(data) {
    // Lägg till dem nya meddelandena
    console.log(data)
    if (data["target"] == username) {
        window.location.href = data["url"];
    }
});


// Emit a request to get all currently chatting users
socket.emit("get_users");

function myFunction(user) {
    window.location.href = '/' + user;
}


socket.on("request_private_chat", function(data) {
    console.log(data);

    if (data["recipent"] == username) {
        document.getElementById("messages").innerHTML += '<div class="message" id="highlight-connect"><span class="message-username">' + data["requester"] + " wants to private chat " + "<a href =" + "/" + data["key"] + ">" + "click here" + "</a>" + '</span></div>';
        updateScroll();
    }
});

// Receive the list of currently chatting users from the server
socket.on("all_users", function(users) {
    var userList = document.querySelector(".chat-users ul");
    userList.innerHTML = "";
    for (var i in users) {
        var user = document.createElement("li");
        user.textContent = users[i];
        var privateChatBtn = document.createElement("button");
        privateChatBtn.textContent = "Private chat!";
        privateChatBtn.id = "privatechat"; // add an id to the button
        //Create a hidden attribute for the username  on the button
        privateChatBtn.setAttribute("data-username", users[i]);

        privateChatBtn.setAttribute('onclick', 'myFunction("' + users[i] + '")');



        privateChatBtn.id = "privatechat"; // add an id to the button
        user.appendChild(privateChatBtn);
        userList.appendChild(user);
    }
});

function preventHTML(message) {
    var newMessage = message;
    newMessage = newMessage.replace(/&/g, "&amp;");
    newMessage = newMessage.replace(/</g, "&lt;");
    newMessage = newMessage.replace(/>/g, "&gt;");
    newMessage = newMessage.replace(/"/g, "&quot;");
    newMessage = newMessage.replace(/'/g, "&#039;");
    return newMessage;
}

document.getElementById("message-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-button").click();
    }
});

document.getElementById("send-button").addEventListener("click", function(event) {
    event.preventDefault();
    var messageInput = document.getElementById("message-input").value;
    socket.emit("message", preventHTML(messageInput));
    document.getElementById("message-input").value = "";
});
