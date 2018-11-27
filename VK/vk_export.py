# First we need to get an access token based on our application
#
# https://oauth.vk.com/authorize?client_id=token&display=page&redirect_uri=
# https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52
#
# Application ID:	
#
# scope = 2 (friends) + 4 (photos) + 262144 (groups) + 65536 (offline)
#
# Our access_token=
#
# I am going to test request and vk_requests packages

import vk_requests
import requests
import sqlite3
from time import sleep

# Connecting to a database via sqlite3 module
conn = sqlite3.connect("../phpLiteAdmin/HSE.db")

# Creating a cursor for executing SQL commands
cur = conn.cursor()


def main():

    # Assigned token var
    token =

    # List of params needed for the request
    params = {"group_id": 1, "count": 10, "fields": ['sex'], "v": 5.92, "access_token": token}

    # Making a GET request
    r = requests.get('https://api.vk.com/method/groups.getMembers', params=params)

    # Creating session using vk_requests
    api = vk_requests.create_api(service_token=token, scope=['friends', 'photos', 'groups', 'offline'], api_version='5.92')

    # Getting number of members
    count = api.groups.getMembers(group_id='hseofficial')['count']

    # Filling the database with the users
    # Only 1000 at a time, thus I use offset to get all members

    i = 0
    while i < count:
        g_users = api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=i, fields=['sex', 'photo_max_orig'],
                                        count=1000)
        db_upload(g_users)
        print(g_users)
        sleep(0.1)
        i += 1000

    # Uploading the rest of members
    db_upload(api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=(i-1000), fields=['sex', 'photo_max_orig'],
                                    count=(count - i + 1000)))

    # Cleaning the database
    cleanup()

    """
    link_l = []
    for row in cur.execute("SELECT * FROM members ORDER BY RANDOM() LIMIT 5"):
        print(row[5])
        link_l.append(row[5])
    """


# Database upload func
def db_upload(resp):
    for i in resp["items"]:
        cur.execute("INSERT INTO members (vk_id, first_name, last_name, sex, photo_link) VALUES (:id, :f_n, :l_n, :s, :p_l)",
                    {"id": i.get('id'), "f_n": i.get('first_name'), "l_n": i.get('last_name'), "s": i.get("sex"), "p_l": i.get("photo_max_orig")})

        # Saving changes
        conn.commit()


# Cleaning the database
# I need to exclude males, females without an avatar and DELETED accounts
def cleanup():
    # Excluding DELETED
    cur.execute("DELETE FROM members WHERE first_name = 'DELETED'")

    # Excluding male
    cur.execute("DELETE FROM members WHERE sex = 2")

    # Excluding females without an avatar
    cur.execute("DELETE FROM members WHERE photo_link = 'https://vk.com/images/camera_400.png?ava=1'")

    # Excluding deactivated females
    cur.execute("DELETE FROM members WHERE photo_link = 'https://vk.com/images/deactivated_400.png'")

    # Saving changes
    conn.commit()


if __name__ == "__main__":
    main()
