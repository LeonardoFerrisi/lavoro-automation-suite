import streamlit as st
import database as db
import app as a
from dotenv import load_dotenv 
import os

st.header("Your Info")

state = a.check_state()

LOGGEDIN = a.check_state()

if LOGGEDIN:
    st.write("Your Information is below")
    usr = a.check_usr().replace("\n", "")
    info = db.get_user(usr)
    files = info["data"]
    if files:
        st.selectbox(label="Available Files", options=info["data"])
    else:
        st.info("No files to display!")
        st.write("Create one?")
else:
    st.write("Nothing to display")