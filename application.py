import os
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask, redirect, render_template, request
from member import Member

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses are not cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


mem1 = Member(0, 0, "")
mem2 = Member(0, 0, "")
link_list = [mem1, mem2]


@app.route("/", methods=["GET"])
def index_get():
    global link_list
    global mem1
    global mem2
    conn = sqlite3.connect("./phpLiteAdmin/HSE.db")
    c = conn.cursor()
    i = 0
    for row in c.execute("SELECT * FROM members ORDER BY RANDOM() LIMIT 2"):
        link_list[i].un_id = row[0]
        link_list[i].link = row[5]
        link_list[i].rating = row[6]
        i += 1

    return render_template("index.html", link1=mem1.link, link2=mem2.link, id1=mem1.un_id, id2=mem2.un_id)


@app.route("/", methods=["POST"])
def index_post():
    data = request.get_json()
    if data["id"] == "left":
        val1 = 1
        val2 = 0
    else:
        val1 = 0
        val2 = 1

    ratings = elo_rate(mem1.rating, mem2.rating, val1, val2)
    conn = sqlite3.connect("./phpLiteAdmin/HSE.db")
    cur = conn.cursor()
    j = 0
    for i in ratings:
        cur.execute("UPDATE members SET rating = :r WHERE tab_id = :id", {"r": i, "id": link_list[j].un_id})
        conn.commit()
        j += 1
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/hottest", methods=["GET"])
def hot():
    conn = sqlite3.connect("./phpLiteAdmin/HSE.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM members ORDER BY rating DESC LIMIT 1"):
        link = row[5]

    return render_template("hottest.html", link=link)


@app.route("/personal", methods=["GET"])
def personal():
    link = "https://pp.userapi.com/c837221/v837221656/56977/sivXGmIbPEs.jpg"
    return render_template("personal.html", link=link)


@app.route("/github", methods=["GET"])
def github():
    return redirect("https://github.com/Snowfighter/CS50-Final-Project")


def elo_rate(rate1, rate2, val1, val2):
    E1 = 1/(1 + pow(10, ((rate1 - rate2)/400)))
    E2 = 1/(1 + pow(10, ((rate2 - rate1)/400)))

    rate1_new = rate1 + 32*(val1 - E1)
    rate2_new = rate2 + 32 * (val2 - E2)

    return [rate1_new, rate2_new]
