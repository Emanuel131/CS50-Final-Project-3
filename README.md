<a href='https://secure-island-71749.herokuapp.com'>
    <img src='./media/logo.png' alt='HSE SMASH Logo' title='HSE SMASH' align='right' height='60'/>
</a>

# HSE SMASH (CS50 Final Project)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
![GitHub last commit](https://img.shields.io/github/last-commit/Snowfighter/CS50-Final-Project)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

:star: Star me on GitHub — just for fun and motivation :grinning:

[HSE SMASH](https://secure-island-71749.herokuapp.com) is my final project for Harvard CS50 online course. It is a web app that allows you to compare girls by there profile photos & find the hottest one :fire: :fire: :fire: :fire: :smirk: :smirk: :smirk: :smirk:

<a href='https://secure-island-71749.herokuapp.com'>
    <img src='./media/front_page.png' alt='Front Page'/>
</a>

## Table of contents

-   [Idea](#idea)
-   [Structure](#structure)
    -   [Database](#phpLiteAdmin)
    -   [VK](#vk)
        - [Main](#main)
        - [Upload func](#db_upload)
        - [Cleanup](#cleanup)
    -   [Application](#application.py)

## Idea

The idea of making such an app came to me after watching ["The Social Network"](https://www.imdb.com/title/tt1285016/) movie. Where Mark Zuckerberg gets pissed off by his ex girlfriend and, being a little bit drunk, creates FaceSmash, a web-app that allows to compare Harvard girls between each other, two at a time. 

I was not pissed by my ex, nor was I drunk, but decided to reimplement this app using Python as a backend language for my Flask Server and JS/HTML/CSS for my pages. Being a HSE student I have decided to use VK society for getting the profile pages of the girls from my university. 

Below I give a detailed description of all the project, so feel free to use it as a template for making such a prank in your own university :wink:

## Structure
```
├── phpLiteAdmin
│   └── HSE.db
├── VK
│   └── vk_export.py

├── application.py
├── member.py
├── templates
│   └── credits.html
│   └── hottest.html
│   └── index.html
│   └── layout.html
│   └── personal.html
├── static
│   ├── fonts
│   │   └── SexyShoutFreeFont.ttf
│   │   └── SexyShoutFreeFont.otf
│   └── Jobs.jpg
│   └── Jobs2.jpg
│   └── Slushi.jpg
│   └── scripts.js
│   └── styles.css
├── LICENSE
├── README.md

```

### phpLiteAdmin
Before writing my web app I need a database with my girls. For that I need to decide what tools to use and what fields to create for each member. 

I have decided to use [SQLite](https://www.sqlite.org/index.html) for this project and [phpLiteAdmin](https://www.phpliteadmin.org) for local management and testing. The latter was utilized for initial cretion of the db, table and fields, though it could be done programmatically in Python. Here is the link for how to start a local phpLiteAdmin server "https://bitbucket.org/phpliteadmin/public/wiki/NoWebserver". 

The snipet of resulting "members" table: 

| tab_id | vk_id | first_name | last_name       | sex | photo_link | rating |
| ------ | ----- | ---------- | --------------  | --- | ---------- | ------ |
| 	2	 | 270	 | Irina	  |   Rybakova	    | 1	  | https://pp.userapi.com/c629116/v629116270/14349/NivavpUia9k.jpg?ava=1	                    | 2.0 |
| 	5	 | 509	 | Alyona	  |   Vershinina	| 1	  | https://pp.userapi.com/c852128/v852128160/2b6c0/pnVQlSodoEE.jpg?ava=1	                    | 0.0 |
| 	7	 | 605	 | Lena	      |   Udodova	    | 1	  | https://sun1-11.userapi.com/kDDxts6O4jouBIScMt4iH7nRVT_JKxzKkv9gaw/_IWoF3dFzlA.jpg?ava=1	| 0.0 |
| 	8	 | 680	 | Katya	  |   Semenko	    | 1	  | https://pp.userapi.com/c627316/v627316680/43095/ZVEhuFxe59Y.jpg?ava=1	                    | 0.0 |
| 	9	 | 692	 | Liza	      |   Kulik	        | 1	  | https://pp.userapi.com/c630416/v630416692/7446/Rbatb84-q9k.jpg?ava=1	                    | 0.0 |
| 	13	 | 796	 | Alina	  |   Sazonova	    | 1	  | https://pp.userapi.com/c638923/v638923796/4ebfc/Pa1bYmNPZgE.jpg?ava=1	                    | 0.0 |
| 	16	 | 896	 | Olga	      |   Borodulina	| 1	  | https://pp.userapi.com/c313/u00896/a_2f90c1d9.jpg?ava=1	                                    | 0.0 |
| 	17	 | 905	 | Alina	  |   Yashina	    | 1	  | https://pp.userapi.com/c824504/v824504324/1a43e4/x0DNcr_UhG0.jpg?ava=1	                    | 0.0 |

### VK
Now let's look at [vk_export.py](./VK/vk_export.py) which populates my database with girls. 

I use [vk-requests](https://pypi.org/project/vk-requests/) package for making VK API calls and [sqlite3](https://docs.python.org/3/library/sqlite3.html) for making queries. 

``` python
import vk_requests
import sqlite3
from time import sleep
```
Then I create a connect to the database and create a cursor for making queries.

```python
conn = sqlite3.connect("../phpLiteAdmin/HSE.db")
cur = conn.cursor()
```
#### Main

I the `main` function I get access to the api calls by using the `token` for my application which I got from registering the application with [VK API](https://vk.com/dev/access_token). In `create_api` I also specify the `scope` (with I would like to work in my app) and the `api_version`.

Getting the all the users from the [HSE Official Group](https://vk.com/hseofficial) posed a little change, because I could only get 1000 users per one request. That is why I have decided to get the whole number of comminuty members first  and then, using the while loop, make requests with an `offset`. 

In the while loop I use `getMembers` method, where I specify `group_id`, `sort` order, `offset`, `fields` that I need for the db and `count` - max number of users I can get per one request.

Next I use `db_upload` function for populating my local db and print into console for error checking. I also had an issue with "making too many requests" bugs, so I used `sleep()` function for a little pause in execution. After that I increment `i`, which is my offset variable.

In the end of the `main` function I make one last API call for the rest of the users (I use 1000 as the increment, but the number of users is not a round one). I also use a `cleanup` function for beautifying the database. 

``` python
def main():

    token = ...

    api = vk_requests.create_api(service_token=token, scope=['friends', 'photos', 'groups', 'offline'], api_version='5.92')

    count = api.groups.getMembers(group_id='hseofficial')['count']

    i = 0
    while i < count:
        g_users = api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=i, fields=['sex', 'photo_max_orig', 'bday'],
                                        count=1000)
        db_upload(g_users)
        print(g_users)
        sleep(0.1)
        i += 1000

    db_upload(api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=(i-1000), fields=['sex', 'photo_max_orig'],
                                    count=(count - i + 1000)))

    cleanup()
```

#### db_upload
`db_upload` function gets a response from the API request and for every user in my 1000 returned ones executes an insertion into my "members" table. For this I utilize the `cursor` which I have defined earlier and using an `execute` method I write a simple query. Also never forget to do `conn.commit()` for saving the changes (reminds me of a `git commit` command).   

```python
def db_upload(resp):
    for i in resp["items"]:
        cur.execute("INSERT INTO members (vk_id, first_name, last_name, sex, photo_link) VALUES (:id, :f_n, :l_n, :s, :p_l)",
                    {"id": i.get('id'), "f_n": i.get('first_name'), "l_n": i.get('last_name'), "s": i.get("sex"), "p_l": i.get("photo_max_orig")})

        conn.commit()
```

#### cleanup

The `cleanup` function makes some changes to the table through a number of SQL queries:

1. Deletes all DELETED accounts
2. Deletes all males (`sex` parameter equals 2)
3. Deletes all users with no picture
4. Deletes all users with deactivated profile picture

```python
def cleanup():

    cur.execute("DELETE FROM members WHERE first_name = 'DELETED'")

    cur.execute("DELETE FROM members WHERE sex = 2")

    cur.execute("DELETE FROM members WHERE photo_link = 'https://vk.com/images/camera_400.png?ava=1'")

    cur.execute("DELETE FROM members WHERE photo_link = 'https://vk.com/images/deactivated_400.png'")

    conn.commit()
```

### application.py
This file is the route of our backend Flask server. It contains commands for every page the user visits and the method the user uses to visit them (POST or GET).

So at first I need to import [flask](https://flask.palletsprojects.com/en/1.1.x/) package for our server, [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) for working with the database and also `json` and `Member` class from helping [member.py](./member.py).

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request
import json
from member import Member
```

Then I make some default initial configs:

1. Configure the application
2. Ensure the templates are reloaded
3. Disable commit tracking (Turn off Flask-SQLAlchemy event system for saving resources)
4. Adding path to the database (Local or Remote, Ex. Heroku DB)
5. Initiating DB object
6. Creating a [table class](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/) in order to read/write into the database 

```python
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./phpLiteAdmin/HSE.db'

db = SQLAlchemy(app)

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
```

Now let's look at the rest of the code with the `app` decorators, but before doing that I make sure that no responses are cached and make global vars for two compared girls using `Member` class.

```python
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

mem1 = Member(0, 0, "")
mem2 = Member(0, 0, "")

link_list = [mem1, mem2]
```
In addition I'll also discuss the `Member` class in order to avoid futher confusion. It has only three parameters: 
- un_id -- unique ID in "members" table
- rating -- a double number
- link -- a url of the profile picture

```python
class Member:
    def __init__(self, un_id, rating, link):
        self.un_id = un_id
        self.rating = rating
        self.link = link
```

Let's return back to [application.py](./application.py).

If the user visits the main ([index](./templates/index.html)) page via GET, he/she gets presented with two random profile picture of girls, which the app gets by making a query to the "members" table. It assigns the corresponding values to the variables in `link_list` and, in the end renders a template with the right links and ids.

```python
@app.route("/", methods=["GET"])
def index_get():
    global link_list
    i = 0
    girls = Members.query.order_by(func.random()).limit(2)
    for g in girls:
        link_list[i].un_id = g.tab_id
        link_list[i].link = g.photo_link
        link_list[i].rating = g.rating
        i += 1

    return render_template("index.html", link1=mem1.link, link2=mem2.link, id1=mem1.un_id, id2=mem2.un_id)
```

If the user visits the main ([index](./templates/index.html)) page via POST, so as by clicking on a button under the picture of the girl he/she likes more, my app needs to deal with how to give the girl the rating points and also reload the page to output the next random pair.

Using JSON we get data from POST request, which has information about which picture the user has choosen. This data contains `s1` and `s2` coefficients, which correspond to the 1st and the 2nd profile picture and can be either 1 or 0. 

Using the received coefficients and the current girls' ratings I calculate their new ratings using the Elo Rating Algorithm and after that write the new numbers into the local database.
In the end I dump a json that everything went without mistakes.

```python
@app.route("/", methods=["POST"])
def index_post():
    data = request.get_json()

    ratings = elo_rate(mem1.rating, mem2.rating, data["s1"], data["s2"])
    j = 0
    for i in ratings:
        girl = Members.query.filter_by(tab_id=link_list[j].un_id).first()
        girl.rating = i
        db.session.commit()
        j += 1

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
```
#### Elo Rating Algorithm

Basically it means that if you have two girls, where one has a high rating and another one has a low rating and, supposedly, the girl with highest rating wins, she gets less points in comparison with the situation, when the girl with the low rating wins. It is a coommon rating system in strategic games and it is best explained in this video: https://www.youtube.com/watch?v=GTaAWtuLHuo&index=4&list=LLwfqVIYgpcUBxvjAdSkO05w

```python
def elo_rate(rate1, rate2, s1, s2):
    E1 = 1/(1 + pow(10, ((rate1 - rate2)/400)))
    E2 = 1/(1 + pow(10, ((rate2 - rate1)/400)))

    rate1_new = rate1 + 32*(s1 - E1)
    rate2_new = rate2 + 32 * (s2 - E2)

    return [rate1_new, rate2_new]
```

The last routes in my app to be discussed are pretty straightforward. 

In the [hottest](./templates/hottest.html) I render a photo of a girl with the highest rating, which a get by making an ordering query to the table.

In the [personal](./templates/personal.html) I have hardcoded my personal choice, `github` just redirects to this page and, finally in the [credits](./templates/credits.html) I have a thanking message to the CS50 staff.

```python
@app.route("/hottest", methods=["GET"])
def hot():
    girl = Members.query.order_by(desc(Members.rating)).first()

    return render_template("hottest.html", link=girl.photo_link)

@app.route("/personal", methods=["GET"])
def personal():
    link = "https://pp.userapi.com/c847020/v847020538/1427a1/lVggmbf3o-U.jpg"
    return render_template("personal.html", link=link)

@app.route("/github", methods=["GET"])
def github():
    return redirect("https://github.com/Snowfighter/CS50-Final-Project")


@app.route("/credits", methods=["GET"])
def credit():
    return render_template("credits.html")
```