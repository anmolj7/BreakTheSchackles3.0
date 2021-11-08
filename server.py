from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_meeting")
def add_meeting():
    return render_template("add_meeting.html")

if __name__ == "__main__":
    app.run(debug=True)