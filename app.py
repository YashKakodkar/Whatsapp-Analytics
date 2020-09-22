import os
from flask import Flask, render_template, request
from analyze import make_file, analyze, compile_data, to_json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analytics", methods=['POST'])
def analytics():
    target = os.path.join(APP_ROOT, 'static/files')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        make_file(filename)
        analyze()
        data = compile_data()
        chat_name = data['chatName']
        date_created = data['dateCreated']
        messages_sent = data['messagesSent']
        members = data['currentMemberCount']
        chat_type = "Group Chat"
        if members == 2:
            chat_type = "Private Message"

    return render_template("analytics.html",
                           chat_name=chat_name,
                           chat_type=chat_type,
                           messages_sent=messages_sent,
                           members=members,
                           date_created=date_created,
                           data=data
                           )
