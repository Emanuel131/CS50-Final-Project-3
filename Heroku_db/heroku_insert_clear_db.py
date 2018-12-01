import vk_requests
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from heroku_declaritive_db import Base, Members

# Connecting to a Heroku db
engine = create_engine(
    'url to your db',
    echo=False)

# Binding engine to a Base class
Base.metadata.bind = engine

# Creating session
DBSession = sessionmaker(bind=engine)
session = DBSession()


def main():

    # Assigned token var
    token = 'your vk api token'

    # Creating session using vk_requests
    api = vk_requests.create_api(service_token=token, scope=['friends', 'photos', 'groups', 'offline'], api_version='5.92')

    # Getting number of members
    count = api.groups.getMembers(group_id='hseofficial')['count']

    # Filling the database with the users
    # Only 1000 at a time, thus I use offset to get all members
    i = 0
    while i < count:
        g_users = api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=i,
                                        fields=['sex', 'photo_max_orig'],
                                        count=1000)
        db_upload(g_users)
        sleep(0.1)
        i += 1000

    # Uploading the rest of members
    db_upload(api.groups.getMembers(group_id='hseofficial', sort='id_asc', offset=(i - 1000),
                                        fields=['sex', 'photo_max_orig'],
                                        count=(count - i + 1000)))

    # Cleaning the database
    cleanup()


# Upload function
def db_upload(resp):
    for i in resp['items']:
        new_member = Members(vk_id=i.get('id'), first_name=i.get('first_name'), last_name=i.get('last_name'), sex=i.get("sex"), photo_link=i.get("photo_max_orig"))
        session.add(new_member)
        session.commit()


# Cleaning the database
# I need to exclude males, females without an avatar and DELETED accounts
def cleanup():
    # Excluding DELETED
    session.query(Members).filter(Members.first_name == 'DELETED'). \
        delete(synchronize_session=False)

    # Excluding male
    session.query(Members).filter(Members.sex == 2). \
        delete(synchronize_session=False)

    # Excluding females without an avatar
    session.query(Members).filter(Members.photo_link == 'https://vk.com/images/camera_400.png?ava=1'). \
        delete(synchronize_session=False)

    # Excluding deactivated females
    session.query(Members).filter(Members.photo_link == 'https://vk.com/images/deactivated_400.png'). \
        delete(synchronize_session=False)

    # Saving changes
    session.commit()


if __name__ == '__main__':
    main()
