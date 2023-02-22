from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
import time
import os
import random
import argparse

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.use_x_sendfile = False
socketio = SocketIO(app)

messages = []

#add any words that will be filtered 
SPAM_KEYWORDS =['Fuck']

@app.route("/")
def home():
    #Om man redan är inloggad
    if "username" in session:
        return redirect("/chat")
        
    return render_template("login.html")

@socketio.on("message") #Om vi får socket emit med message (någon har skickat ett meddelande)
def handle_message(data):
    #prevent html injections
    data["message"] = data["message"].replace("<", "&lt;")
    data["message"] = data["message"].replace(">", "&gt;")
    if not contains_spam(data):
        messages.append(data) #Så dem som ansluter senare kan se alla gammla meddelanden
        emit("new_message", data, broadcast=True) #Meddela att ett nytt meddelande har skickats till alla (broadcast)
    
@app.route("/chat", methods=["POST", "GET"])
def chat():

    #print(request.form)
    if request.method == 'POST':
    
        #Om någon nyss loggat in
        if("username" in request.form):
            session['username'] = request.form['username']

            username = session['username']
            socketio.emit("new_connect", f"{username} connected to the chat!", broadcast=True) 
    
    return render_template("chat.html", username=session['username'],messages=messages)
    
def contains_spam(data):
    for keyword in SPAM_KEYWORDS:
        if keyword.lower() in data["message"].lower():
            return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    args = parser.parse_args()

    socketio.run(app, debug=True, host=args.host, port=args.port)

