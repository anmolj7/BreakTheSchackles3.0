from flask import Flask, render_template, url_for, redirect, request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from threading import Thread
import time
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = "A super long secret key no one is supposed to know"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
scheduler = APScheduler()


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50))
    class_link = db.Column(db.String(50))
    class_time = db.Column(db.DateTime)
    recording_time = db.Column(db.DateTime)
    started = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)


def get_meeting_list(finished=False):
    meeting_list = []
    for meeting in Meeting.query.all():
        if meeting.finished == finished:
            meeting_list.append(
                {
                    'id': meeting.id,
                    'class_name': meeting.class_name,
                    'class_link': meeting.class_link,
                    'class_time': meeting.class_time,
                    'started': meeting.started,
                    'finished': meeting.finished
                }
            )
    # Sort the list on the basis of the meeting times
    meeting_list = sorted(meeting_list, key=lambda x: x['class_time'])
    return meeting_list


MEETINGS = []


@app.route("/")
def home():
    return render_template("add_meeting.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])


@app.route("/completed_meetings")
def completed_meetings():
    return render_template("completed_meetings.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])

@app.route("/add_meeting")
def add_meeting():
    return render_template("add_meeting.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])


@app.route("/form_add_meeting", methods=["POST"])
def form_add_meeting():
    class_name = request.form.get('class_name')
    class_link = request.form.get('class_link')
    class_time = request.form.get('class_time')
    class_time = datetime.strptime(class_time, "%Y-%m-%dT%H:%M")
    if len(Meeting.query.all()) == 0:
        _id = 0
    else:
        _id = Meeting.query.all()[-1].id
        print(_id)
    meeting = Meeting(id=_id+1, class_name=class_name,
                      class_link=class_link, class_time=class_time)
    db.session.add(meeting)
    db.session.commit()
    return redirect(url_for('add_meeting'))


@app.route('/delete_meeting', methods=['POST'])
def delete_meeting():
    class_id = request.form.get("meeting_id")
    meeting = Meeting.query.filter_by(id=class_id).first()
    db.session.delete(meeting)
    db.session.commit()
    return redirect(url_for("add_meeting"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5001)
