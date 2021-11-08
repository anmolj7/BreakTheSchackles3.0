from flask import Flask, render_template, url_for, redirect, request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from JoinMeet import JoinMeet
from datetime import datetime
from threading import Thread
from autotrans import download
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


class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    recording_link = db.Column(db.String(50))

class TranscribedVideo(db.Model):
    name = db.Column(db.String(100))
    file_name = db.Column(db.String(100), primary_key=True)


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
PROCESSING = []


def start_recording(meeting):
    print("Starting recording")
    user = User.query.first()
    MEETINGS.append(JoinMeet(user.email, user.password))
    MEETINGS[-1].join_meet(meeting.class_link, meeting.id)
    MEETINGS[-1].record_meeting(user.recording_link)


def checker():
    for meeting in Meeting.query.all():
        if datetime.now() > meeting.class_time and not meeting.started:
            meeting.started = True
            db.session.commit()
            start_recording(meeting)


@app.route("/")
def home():
    return render_template("add_meeting.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])


@app.route("/completed_meetings")
def completed_meetings():
    videos = TranscribedVideo.query.all()
    video_list = []
    for video in videos:
        data = ""
        with open(video.file_name.replace("mp4", "txt")) as f:
            data = f.read()
        video_list.append(
            {
                'video_name': video.name,
                'video_file_name': video.file_name.replace("mp4", "txt"),
                'video_file_text': data
            }
        )
    print(video_list)
    return render_template("completed_meetings.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'], finished_meetings=get_meeting_list(True), video_list=video_list, PROCESSING=PROCESSING)


@app.route("/add_meeting")
def add_meeting():
    return render_template("add_meeting.html", meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])


@app.route("/user")
def user():
    user = User.query.first()
    return render_template("user.html", user=user, meeting_list=get_meeting_list(), colors=['yellow', 'blue', 'red', 'green'])


@app.route("/add_user", methods=['POST'])
def add_user():
    email = request.form.get('email')
    password = request.form.get('password')
    recording_link = request.form.get('recording_link')

    user = User(email=email, password=password, recording_link=recording_link)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))


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


@app.route('/transcribe_video', methods=["POST"])
def transcribe_video():
    def process_video(name, video_file_name):
        PROCESSING.append(video_file_name)
        print("Starting processing! ")
        from Transcribe import Transcribe
        transcribed_text = Transcribe(video_file_name)
        with open(video_file_name.replace("mp4", "txt"), "w+") as f:
            f.write(transcribed_text)
        video = TranscribedVideo(name=name, file_name=video_file_name)
        db.session.add(video)
        db.session.commit()
        PROCESSING.pop()
        os.remove(video_file_name)
        return

    meeting_id = request.form.get('meeting_id')
    meet = Meeting.query.filter_by(id=meeting_id).first()
    name = meet.class_name
    recording_time = meet.recording_time
    user = User.query.first()
    meet_link = user.recording_link
    meet_link = meet_link[len("https://meet.google.com/"):]
    obj = download(user.email, user.password, meet.recording_time.strftime(
        "%H:%M"), f"{meet_link}", meet.recording_time.strftime("%Y-%m-%d"))
    obj.google_login()
    obj.downloadfile()
    filename = meet.recording_time.strftime(
        f"{meet_link} (%Y-%m-%d at %H_%M GMT-8).mp4")
    db.session.delete(meet)
    db.session.commit()
    thread = Thread(target=process_video, kwargs={
                    'video_file_name': filename, 'name': name})
    thread.start()
    return redirect(url_for('completed_meetings'))


@app.route('/view_file/<filename>')
def view_file(filename):
    with open(filename) as f:
        return f.read()

if __name__ == "__main__":
    db.create_all()
    scheduler.add_job(id="check_time", func=checker,
                      trigger="interval", seconds=5)
    scheduler.start()
    app.run(debug=True, port=5007, use_reloader=False)
