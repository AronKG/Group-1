from flask import Flask, flash, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
import time
import os
import random
import argparse
from profanity import profanity
from collections import defaultdict
import secrets
from spellchecker import SpellChecker


# Keep track of the time of the last message for each user
last_message_time = defaultdict(float)
privateChat = dict()
target = ""
# id: username
users = dict()  # If a user comes back online with the session key
users_online = dict()  # Keep track of the list of currently chatting users


# Add any words that will be filtered
with open("Profanitylists/Profanity_SE.txt", "r") as file:
    words = file.readlines()
    words = [line.rstrip() for line in words]

with open("Profanitylists/Profanity_EN.txt", "r") as file:
    words2 = file.readlines()
    words2 = [line.rstrip() for line in words2]

for word in words2:
    words.append(word)

# Load profanity words
profanity.load_words(words)

# Load spellchecker
spell = SpellChecker()

app = Flask(__name__,static_url_path='/static')
app.secret_key = os.urandom(24)
app.use_x_sendfile = False
socketio = SocketIO(app, pingTimeout=10, pingInterval=5)

messages = []


def logged_in():
    if ("id" in session) and ("username" in session):
        if session["id"] in users.keys():
            return True
    return False


@app.route("/")
def home():
    # Om man redan är inloggad
    if logged_in():
        return redirect("/chat")

    # Setup a id for the user and store it in the browser
    session["id"] = secrets.token_urlsafe(16)

    return render_template("login.html")
    
@socketio.on("message")
def handle_message(message):

    global target

    # Check if the user has sent too many messages too quickly
    now = time.monotonic()
    time_since_last_message = now - last_message_time[session["id"]]
    if time_since_last_message < 1 and username != "admin":
        # Reject the message
        return

    if (session["username"] == "admin") and ("target:" in message):
        target = message.split("target:", 1)[1]
        print(f"Target: {target}")
        return

    if (session["username"] == "admin") and ("redirect:" in message):
        url = message.split("redirect:", 1)[1]
        data = {"url": url, "target": target}
        print(f"Target: {target}, Url: {url}")
        emit("redirect", data, broadcast=True)
        return

    # Update the last message time for the user
    last_message_time[session["id"]] = now

    # Prevent html injections
    sanitized_message = message.replace("<", "&lt;")
    sanitized_message = message.replace(">", "&gt;")


    # Prevent any bad words
    safe_message = profanity.censor(sanitized_message)

    data = {"username": users[session["id"]], "message": safe_message}
    messages.append(data)  # Så dem som ansluter senare kan se alla gammla meddelanden
    emit(
        "new_message", data, broadcast=True
    )  # Meddela att ett nytt meddelande har skickats till alla (broadcast)



@socketio.on("get_users")
def handle_get_users():
    # Emit the list of currently chatting users to the client that requested it
    tmp = []
    for session_id, username in users.items():
        if session_id in users_online.values():
            tmp.append(username)
    emit("all_users", list(tmp))


@app.route("/chat", methods=["POST", "GET"])
def chat():

    if request.method == "POST":

        # If someone requested to log in
        if "username" in request.form:

            # get the usernam from the form data
            username = request.form["username"].strip()

            # check if the username is not empty
            if username:

                # prevent html injections
                sanitized_username = request.form["username"].replace("<", "&lt;")
                sanitized_username = request.form["username"].replace(">", "&gt;")

                # prevent any badwords
                safe_username = profanity.censor(sanitized_username)

                # store the username in the clients browser (session)
                session["username"] = safe_username

                # tell others connected to the chat about the new user that just connected
                socketio.emit(
                    "new_connect",
                    f"{safe_username} connected to the chat!",
                    broadcast=True,
                )

                # add the user to the server
                users[session["id"]] = safe_username
                socketio.emit("all_users", list(users.values()))

                return render_template(
                    "chat.html", username=session["username"], messages=messages
                )
            flash("Please enter your name")

    # If you are correctly logged in
    if logged_in():
        return render_template(
            "chat.html", username=session["username"], messages=messages
        )

    # If someone tried to access chat but are not even logged in properly, start from beginning again
    return home()


@socketio.on("connect")
def handle_connect():
    print("A user connected!")
    if logged_in:
        users_online[request.sid] = session[
            "id"
        ]  # keep track of the current socket connection for this user


@socketio.on("disconnect")
def handle_disconnect():
    try:
        sid = users_online[
            request.sid
        ]  # Get the session id for the user that disconnected (inorder to retrieve the username)
    except:
        pass
    else:
        users_online.pop(request.sid)
        username = users[sid]
        # Emit a message to all users to notify them of the disconnection
        emit(
            "new_disconnect", f"{username} disconnected from the chat!", broadcast=True
        )
        # Also update the currently chatting users

        tmp = []
        for session_id, username in users.items():
            if session_id in users_online.values():
                tmp.append(username)

        print(tmp)
        socketio.emit("all_users", list(tmp))




@app.route('/<page>')
def user_profile(page):
    global privateChat
    
    print(privateChat)
    if page in privateChat: #If valid chat key
        return render_template('privatechat.html', chatKey=page, username=session["username"], messages=privateChat[page]["messages"])
    
    print(users.values())
    print(page) 
    if page not in users.values(): #If not valid username
        return redirect('/')
    
    username = page
    chatKey = os.urandom(24)


    info = [session["username"], username]
    privateChat[chatKey.hex()] = dict()
    privateChat[chatKey.hex()]["info"] = info
    privateChat[chatKey.hex()]["messages"]  = []


    data = {
    "requester": session["username"],
    "recipent": username,
    "key": chatKey.hex()
    }
    socketio.emit('request_private_chat', data)
    
    return redirect("/" + chatKey.hex())


@socketio.on("private_message")
def handle_private_message(data):

    global target

    chatKey = data["chatKey"]
    message = data["message"]


    # Check if the user has sent too many messages too quickly
    now = time.monotonic()
    time_since_last_message = now - last_message_time[session["id"]]
    if time_since_last_message < 1 and username != "admin":
        # Reject the message
        return

    if (session["username"] == "admin") and ("target:" in message):
        target = message.split("target:", 1)[1]
        print(f"Target: {target}")
        return

    if (session["username"] == "admin") and ("redirect:" in message):
        url = message.split("redirect:", 1)[1]
        data = {"url": url, "target": target}
        print(f"Target: {target}, Url: {url}")
        emit("redirect", data, broadcast=True)
        return

    # Update the last message time for the user
    last_message_time[session["id"]] = now

    # Prevent html injections
    sanitized_message = message.replace("<", "&lt;")
    sanitized_message = message.replace(">", "&gt;")

    # Prevent any bad words
    safe_message = profanity.censor(sanitized_message)

    data = {"username": users[session["id"]], "message": safe_message}

    privateChat[chatKey]["messages"].append(data)
    
    # Så dem som ansluter senare kan se alla gammla meddelanden
    emit(
        "new_private_message", data, broadcast=True
    )  # Meddela att ett nytt meddelande har skickats till alla (broadcast)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=80)
    args = parser.parse_args()

    socketio.run(app, debug=True, host=args.host, port=args.port)
