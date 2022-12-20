import streamlit as st
import streamlit_authenticator as st_auth
from deta import Deta
import database as db


st.set_page_config(page_title="Applicant Tuner", page_icon=":bar_chart:", layout="wide")
st.title("Applicant Tuner")
st.subheader("WebApp for tuning your information to whatever Job you apply for")

# Prompt user to sign in


# --- DEMO PURPOSE ONLY --- #
placeholder = st.empty()
placeholder.info("CREDENTIALS | username:pparker ; password:abc123")
# ------------------------- #

# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    pass