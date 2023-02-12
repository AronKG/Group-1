from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
import time
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

messages = []

@app.route("/")
def home():
    #Om man redan är inloggad
    if "username" in session:
        return redirect("/chat")
        
    return render_template("login.html")

@socketio.on("message") #Om vi får socket emit med message (någon har skickat ett meddelande)
def handle_message(data):
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
    

if __name__ == '__main__':
    socketio.run(app, debug=True)

