from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import func
from flask import Flask, redirect, render_template, request
import json
from member import Member

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Disable commit tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Path to the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./phpLiteAdmin/HSE.db'

# Initiating db object
db = SQLAlchemy(app)

# Table class
class Members(db.Model):
    __tablename__ = 'members'
    tab_id = db.Column('tab_id', db.Integer, primary_key=True, nullable=False)
    vk_id = db.Column('vk_id', db.Integer, nullable=False)
    first_name = db.Column('first_name', db.Text, nullable=False)
    last_name = db.Column('last_name', db.Text, nullable=False)
    sex = db.Column('sex', db.Integer, nullable=False)
    photo_link = db.Column('photo_link', db.Text, nullable=False)
    rating = db.Column('rating', db.Float, nullable=False)

    def __init__(self,  tab_id, vk_id, first_name, last_name, sex, photo_link, rating):
        self.tab_id = tab_id
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.photo_link = photo_link
        self.rating = rating


# Ensure responses are not cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Global vars for two girls we are comparing


mem1 = Member(0, 0, "")
mem2 = Member(0, 0, "")

# List of these girls
link_list = [mem1, mem2]


# Getting two random girls in index.html via GET
@app.route("/", methods=["GET"])
def index_get():
    global link_list
    global mem1
    global mem2
    i = 0
    girls = Members.query.order_by(func.random()).limit(2)
    for g in girls:
        link_list[i].un_id = g.tab_id
        link_list[i].link = g.photo_link
        link_list[i].rating = g.rating
        i += 1

    return render_template("index.html", link1=mem1.link, link2=mem2.link, id1=mem1.un_id, id2=mem2.un_id)


# Rating two girls in index.html via POST
@app.route("/", methods=["POST"])
def index_post():
    # Getting ajax response via json
    data = request.get_json()

    # Checking
    if data["id"] == "left":
        val1 = 1
        val2 = 0
    else:
        val1 = 0
        val2 = 1

    ratings = elo_rate(mem1.rating, mem2.rating, val1, val2)
    j = 0
    for i in ratings:
        girl = Members.query.filter_by(tab_id=link_list[j].un_id).first()
        girl.rating = i
        db.session.commit()
        j += 1

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Displaying the girl with the biggest rating in hottest.html
@app.route("/hottest", methods=["GET"])
def hot():
    girl = Members.query.order_by(desc(Members.rating)).first()

    return render_template("hottest.html", link=girl.photo_link)


# Displaying my personal choice in personal.html
@app.route("/personal", methods=["GET"])
def personal():
    link = "https://pp.userapi.com/c837221/v837221656/56977/sivXGmIbPEs.jpg"
    return render_template("personal.html", link=link)


# Link to github
@app.route("/github", methods=["GET"])
def github():
    return redirect("https://github.com/Snowfighter/CS50-Final-Project")


# Elo rating algorithm
# It is greatly explained in this video:
# https://www.youtube.com/watch?v=GTaAWtuLHuo&index=4&list=LLwfqVIYgpcUBxvjAdSkO05w
def elo_rate(rate1, rate2, val1, val2):
    E1 = 1/(1 + pow(10, ((rate1 - rate2)/400)))
    E2 = 1/(1 + pow(10, ((rate2 - rate1)/400)))

    rate1_new = rate1 + 32*(val1 - E1)
    rate2_new = rate2 + 32 * (val2 - E2)

    return [rate1_new, rate2_new]
