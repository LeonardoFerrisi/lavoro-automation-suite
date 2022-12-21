from deta import Deta
from dotenv import load_dotenv 
import os
import streamlit as st

try:
    load_dotenv(".db_env")
except:
    pass
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

db = deta.Base("users_db")
drive = deta.Drive("userdata")

def update_all(credentials):
    users = fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    emails = [user["email"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    localusers = list(credentials["usernames"].keys())

    # st.write(localusers)
    # st.write(credentials)

    for username in localusers:
        email = credentials["usernames"][username]["email"]
        name = credentials["usernames"][username]["name"]
        password = credentials["usernames"][username]["password"]

        if username not in usernames:
            credentials["usernames"][username]["data"] = []
            data = credentials["usernames"][username]["data"]
            insert_user(username, email, name, password, data)
        else:
            data = credentials["usernames"][username]["data"]

            updates = {
                "name":name,
                "email":email,
                "password":password,
                "data":data,
            }
            update_user(username=username, updates=updates)
        # st.write(email, name, password, data)


def insert_user(username, email, name, password, files):
    """
    Returns the user on a successful user creation, otherwise raises an error
    """
    return db.put({"key":username,"name": name, "email":email, "password":password, "data":files})

def fetch_all_users():
    """
    Reutrns a dict of all users
    """
    result = db.fetch()
    return result.items

def get_user(username):
    """
    If not found, the function will return None
    """
    return db.get(username)



def update_user(username, updates):
    """
    If an item is updated, returns None. Otherwise, an exception is raised

    Updates must be formatted in the format
    """
    return db.update(key=username, updates=updates)

def delete_user(username):
    """
    delete a user
    """
    return db.delete(username)

def save_file(filename, filepath, content_type, desc):
    """
    Uploads a file to the database

    Parameters:

        filename: name of the file

        filepath: path to the file

        content_type: What type of content is this (i.e: .json)

        desc: What is in this file (i.e: vaction spots)
    """
    drive.put(name=filename, data=desc, path=filepath, content_type=content_type)

def retrieve_file(filename):
    file = drive.get(filename)
    if file:
        contents = file.read()
        file.close()
        return contents
    return None

def delete_file(filename):
    """
    Deletes a file, if file does not exist nothing happens
    """
    drive.delete(filename)

def delete_files(filenames:list):
    drive.delete_many(filenames)

def list_files(limit=1000):
    result = drive.list()
    all_files = result.get("names")
    paging = result.get("paging") # Contains paging information. 
                                            # Example:
                                                #       "paging": {
                                                #     "size": 2,
                                                #     "last": "file_2.txt"
                                                #   }
    last = paging.get("last") if paging else None # For the last page, last is not present in the response.

    # Iterate through all files until complete
    while (last):
        # provide last from previous call
        result = drive.list(last=last)

        all_files += result.get("names")
        # update last
        paging = result.get("paging")
        last = paging.get("last") if paging else None

    # print("all files:", all_files)

    return all_files


if __name__ == "__main__":
    # A test
    # insert_user(username="test_user1234", email="testuser1345@testuser.com", name="Test Userium", password="a_password12345")
    # print(fetch_all_users())
    # print(get_user("test_user1234"))
    pass