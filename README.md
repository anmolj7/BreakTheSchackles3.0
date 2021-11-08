# BreakTheSchackles3.0
A project that can join a google meet for you, record it, then, when the recording is processed, give you a transcript, saving you from all the trouble of having to attend a class if you don't wanna.
# Problem that it solves
During the pandemic, everything has slowly shifted online, and because of that, there is a lot of screen time, and a lot of meetings every single day, and sometimes, we have to attend the meeting even though we don't want to. Wouldn't our lives be so much easier if we could just program an app to take the class for us, record it, and then give us the transcript? That's exactly what our project aims to achieve.
It is a web app, where you can just schedule the meetings, and it will store all of them in a database, and once it is time for the meeting, it will join the meeting using Selenium, and even set a minimum threshold of "number of attendees" so that if the number of participants goes lower than the threshold, it will automatically leave the meeting too.
# Challenges we ran into
The first and the most challenging problem that we faced was finding a way to record a google meet. We tried a lot of stuff, one of which was attempting to use OpenCV, to capture the video, but that wouldn't have allowed us to record the audio as well. So, to overcome this, we thought of a "hack". What if you just open a new meeting, and then in the new meeting, share your tab, and then, start the recording in that meeting. That way, you won't have to worry about all the nasty stuff like having to deal with recording it yourself and storing it. That way, you automatically get a mail once the recording is processed. There were a lot of problems while implementing this approach, but we eventually managed to get it by using trial and error, and a combination of a lot of libraries.
One other problem that we faced was, just having to deal with bigger audio files to convert them into a transcript, since we can not use the STT services like Google, or even IBM Watson, to convert such big files. So, to get over that, we just broke the file into several chunks, and then, one by one translated them and added them to get the final transcript. 
The issue that we ran into was, that our python view functions only gets called when somebody opens the website, but that wouldn't be feasible if we want to join the class on time, and we cannot use an infinite loop and check every second, because if we do that, then nobody would be able to open the website. So, the only way to solve that problem was to use multithreading, where we create another thread that checks for time every 5 seconds, while the main thread handles the server. We used multithreading for other things like processing the transcript too because if we didn't, the website wouldn't be useable until the file is processed. 
# Technologies we used
<ol>
<li>Python</li>
<li>Flask</li>
<li>SQLite</li>
<li>SQLAlchemy</li>
<li>Selenium</li>
<li>HTML</li>
<li>CSS</li>
<li>Google Text To Speech</li>
<li>Multithreading</li>
</ol>
# Demo
The Demo video of the following project can be seen [HERE](https://www.youtube.com/watch?v=q_MZhyzMEV8)
