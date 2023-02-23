from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
import time
import os
import random
import argparse
from profanity import profanity
from collections import defaultdict

# Keep track of the time of the last message for each user
last_message_time = defaultdict(float)

# Keep track of the list of currently chatting users
users = set()

#add any words that will be filtered
with open("Profanitylists/Profanity_SE.txt", "r") as file:
    words = file.readlines()
    words = [line.rstrip() for line in words]

with open("Profanitylists/Profanity_EN.txt", "r") as file:
    words2 = file.readlines()
    words2 = [line.rstrip() for line in words2]

for word in words2:
    words.append(word)

profanity.load_words(words)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.use_x_sendfile = False
socketio = SocketIO(app)

messages = []

#add any words that will be filtered 

@app.route("/")
def home():
    #Om man redan är inloggad
    if "username" in session:
        return redirect("/chat")
        
    return render_template("login.html")

@socketio.on("message")
def handle_message(data):
    username = data["username"]
    message = data["message"]

    # Check if the user has sent too many messages too quickly
    now = time.monotonic()
    time_since_last_message = now - last_message_time[username]
    if time_since_last_message < 1 and username != "admin":
        # Reject the message
        return

    # Update the last message time for the user
    last_message_time[username] = now

    #prevent html injections
    data["username"] = data["username"].replace("<", "&lt;")
    data["username"] = data["username"].replace(">", "&gt;")
    data["message"] = data["message"].replace("<", "&lt;")
    data["message"] = data["message"].replace(">", "&gt;")
    data["message"] = profanity.censor(data["message"])
    data["username"] = profanity.censor(data["username"])

    messages.append(data) #Så dem som ansluter senare kan se alla gammla meddelanden
    emit("new_message", data, broadcast=True) #Meddela att ett nytt meddelande har skickats till alla (broadcast)

    # Update the list of currently chatting users
    if username not in users:
        users.add(username)
        emit("all_users", list(users), broadcast=True)

@socketio.on("get_users")
def handle_get_users():
    # Emit the list of currently chatting users to the client that requested it
    emit("all_users", list(users))

@app.route("/chat", methods=["POST", "GET"])
def chat():

    #print(request.form)
    if request.method == 'POST':
    
        #Om någon nyss loggat in
        if("username" in request.form):
            session['username'] = request.form['username']

            username = profanity.censor(session['username'])
            socketio.emit("new_connect", f"{username} connected to the chat!", broadcast=True)
            users.add(username)
    
    return render_template("chat.html", username=session['username'],messages=messages)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    args = parser.parse_args()

    socketio.run(app, debug=True, host=args.host, port=args.port)
