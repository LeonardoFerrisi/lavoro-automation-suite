from deta import Deta
from dotenv import load_dotenv 
import os

try:
    load_dotenv(".db_env")
except:
    pass
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

db = deta.Base("users_db")

def insert_user(username, email, name, password):
    """
    Returns the suer on a successful user creation, otherwise raises an error
    """
    return db.put({"key":username,"name": name, "email":email, "password":password})

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
    return db.update(username, updates)

def delete_user(username):
    """
    
    """

if __name__ == "__main__":
    # A test
    # insert_user(username="test_user1234", email="testuser1345@testuser.com", name="Test Userium", password="a_password12345")
    print(fetch_all_users())
    print(get_user("test_user1234"))