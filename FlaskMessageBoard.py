from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

"""
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form["message"]
        messages.append(message)
    return render_template("index.html")

@app.route("/messages")
def messages_route():
    return render_template("messages.html", messages=messages)
"""

if __name__ == '__main__':
    app.run(debug=True)

