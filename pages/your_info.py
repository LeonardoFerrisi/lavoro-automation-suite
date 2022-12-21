import streamlit as st
import database as db
from userapplication import check_state, check_usr
from dotenv import load_dotenv 
import os

st.header("Your Info")

state = check_state()

LOGGEDIN = check_state()

if LOGGEDIN:
    st.write("Your Information is below")
    usr = check_usr().replace("\n", "")
    info = db.get_user(usr)
    files = info["data"]
    if files:
        st.selectbox(label="Available Files", options=info["data"])
    else:
        st.info("No files to display!")
        st.write("Create one?")
else:
    st.write("Nothing to display")