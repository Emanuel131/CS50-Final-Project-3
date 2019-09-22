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
This file is the route of our backend Flask server. It contains commands for every page we visit and the method we use to visit them (POST or GET).

So at first we need to import [flask](https://flask.palletsprojects.com/en/1.1.x/) packsge for our server, [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) for working with the database and also `json` and `Member` class from helping [member.py](./member.py).

