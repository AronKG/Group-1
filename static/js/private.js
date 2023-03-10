//Hämta kontinuerligt nya meddelanden från servern 
var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("new_private_message", function(data) {
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
    data = {
        "message": preventHTML(messageInput),
        "chatKey": chatKey
    };
    socket.emit("private_message", data);

    document.getElementById("message-input").value = "";
});
