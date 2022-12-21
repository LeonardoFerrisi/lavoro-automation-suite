import streamlit as st
import streamlit_authenticator as stauth

import database as db

def prompt_registration(authenticator:stauth.Authenticate, credentials, preauthorization=False):

    current_usernames = credentials["usernames"].keys()
    try:
        if authenticator.register_user(form_name='Register user', location="main", preauthorization=False):
            db.update_all(credentials)
            st.success('User registered successfully')
            # self.prompt_login(authenticator, credentials)
    except Exception as e:
        st.error(e)

if __name__ == "__main__":
    
    users = db.fetch_all_users()
    print(users)
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    emails = [user["email"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    credentials_a = {"usernames":{}}

    for user in users:
        user_data = {
                        "name"    : user["name"],
                        "email"   : user["email"],
                        "password": user["password"],
                        "data"    : user["data"]
                    }
                        
        credentials_a["usernames"][user["key"]] = user_data

    authenticator_a = stauth.Authenticate(credentials=credentials_a, cookie_name="sales", key="abcdef", cookie_expiry_days=30, preauthorized=["default@gmail.com"])

    prompt_registration(authenticator_a, credentials_a, False)