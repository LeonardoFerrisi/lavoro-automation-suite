import streamlit as st
import database as db
import app as a
from dotenv import load_dotenv 
import os
import json
import random

# Functions ------------------
def show_resume(filename):
    file = db.drive.get(filename)
    j = open(filename, "r")

    data = json.load(j)
    st.write(data)
    j.close()

#     # st.write(data)

    # Basics

    # Name
    st.markdown("#### Basic Information:")
    with st.expander(label="Applicant Info"):
        editable_field(title="Name", field="basics", subfield="name", contents=data["basics"]["name"], filename=filename)

        # Label
        editable_field(title="Label", field="basics", subfield="label", contents=data["basics"]["label"], filename=filename)

        # Email
        editable_field(title="Email", field="basics", subfield="email", contents=data["basics"]["email"], filename=filename)

        # Phone
        editable_field(title="Phone", field="basics", subfield="phone", contents=data["basics"]["phone"], filename=filename)

        # Website
        editable_field(title="Website", field="basics", subfield="website", contents=data["basics"]["website"], filename=filename)

        # Summary
        editable_field(title="Summary", field="basics", subfield="summary", contents=data["basics"]["summary"], filename=filename,  area=True)

        # Location

        # Profiles --> have a function that lets you add more

    # with st.expander(label="Work"):
    st.markdown("#### Work")
    work_exp = data["work"]
    for i, exp in enumerate(work_exp):
        company = str(data["work"][i]["company"])
        with st.expander(label=company):
            for label in list(exp.keys()):
                contents = data["work"][i][label]
                editable_field(title=label+" -- *"+company+"*", field="work", subfield=i, subsubfield=label, contents=contents, filename=filename)

    if st.button("Add another?"):
        st.write("TODO: Add field write functionality")


def editable_field(title, field, subfield=None, subsubfield=None, contents="", filename="", area=False):
    """
    Title of editable field
    Data, the actual json
    Field, what we are selecting (i.e: data[name])
    contents: The contents of the thing
    """
    
    if not area:
        content = st.text_input(label=title, value=contents)
    else:
        content = st.text_area(label=title, value=contents)
    # f = open(filename, "r+")
    with open(filename, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        if not subsubfield:
            if not subfield:
                data[field] = content # <--- add `id` value.
            else:
                data[field][subfield] = content
        else:
            data[field][subfield][subsubfield] = content

    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def create_field(ttitle, field, subfield=None, subsubfield=None, contents="", filename="", area=False):
    pass
# ------------------------
# main
# ------------------------

def main():
    st.header("Your Info")

    state = a.check_state()

    LOGGEDIN = a.check_state()

    if LOGGEDIN:
        st.write("Your Information is below")
        usr = a.check_usr().replace("\n", "")
        info = db.get_user(usr)
        files = info["data"]
        if files:
            resumejson = st.selectbox(label="Available Files", options=info["data"])

            show_resume(resumejson)
        else:
            st.info("No files to display!")
            st.write("Create one?")
    else:
        st.write("Nothing to display")

if __name__ == "__main__":
    main()
