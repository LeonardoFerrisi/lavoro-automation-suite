import streamlit as st
import database as db
import app as a
from dotenv import load_dotenv 
import os
import json
import random
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse

# def download(name):
#     app = FastAPI()
    
#     @app.get("/download/{name}")
#     def download_file(name: str):
#         res = db.drive.get(name)
#         return StreamingResponse(res.iter_chunks(4096), media_type="application/json")
    
#     return download_file(name)

# Functions ------------------
def show_resume(filename):
    # download(filename)
    file = db.drive.get(filename)
    j = file.read().decode('utf8')

    data = json.loads(j)
    st.write(data)
    # with open(filename, 'w') as outfile:
    #     json.dump(data, outfile, indent=4)

    keys = float(0001.0)

    # Basics

    # Name
    st.markdown("#### Basic Information:")
    with st.expander(label="Applicant Info"):
        editable_field(title="Name", field="basics", subfield="name", contents=data["basics"]["name"], filename=filename, data=data)

        # Label
        editable_field(title="Label", field="basics", subfield="label", contents=data["basics"]["label"], filename=filename, data=data)

        # Email
        editable_field(title="Email", field="basics", subfield="email", contents=data["basics"]["email"], filename=filename, data=data)

        # Phone
        editable_field(title="Phone", field="basics", subfield="phone", contents=data["basics"]["phone"], filename=filename, data=data)

        # Website
        editable_field(title="Website", field="basics", subfield="website", contents=data["basics"]["website"], filename=filename, data=data)

        # Summary
        editable_field(title="Summary", field="basics", subfield="summary", contents=data["basics"]["summary"], filename=filename, data=data, area=True)

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
                editable_field(title=label+" -- *"+company+"*", field="work", subfield=i, subsubfield=label, contents=contents, filename=filename, data=data, key=str(keys))
                keys = keys + 0.0001

            if st.button(f"Remove {company}", help="You may need to refresh using CTRL+R after removing", key=str(keys)): # optional remove work
                del data["work"][i]
                update_data(filename, data)
        keys = keys + 0.0001
                


    # Add work experience
    work_add_prompt(data, filename)

    # Education
    st.markdown("#### Education")
    edu_key = 2194517523691235.0
    for i, edu in enumerate(data["education"]):
        institution = str(data["education"][i]["institution"])
        with st.expander(label=institution):
            for label in list(edu.keys()):
                contents = data["education"][i][label]
                editable_field(title=label+"-- *"+institution+"*", field="education", subfield=i, subsubfield=label, contents=contents, filename=filename, data=data, key=str(edu_key))
                edu_key+=1.0
            if st.button(f"Remove {institution}", help="You may need to refresh using CTRL+R after removing", key=str(edu_key+10.0)): # optional remove work
                del data["work"][i]
                update_data(filename, data)
    add_education_prompt(data, filename)

    # Awards
    st.markdown("#### Awards")
    award_keys = 1385357871507.0
    # st.write(data["awards"], len(data["awards"]), type(data["awards"]))
    for i, a in enumerate(data["awards"]):
        award = str(data["awards"][i]["title"])
        with st.expander(label=award):
            for label in list(a.keys()):
                contents = data["awards"][i][label]
                editable_field(title=label+"* --"+award, field="awards", subfield=i, subsubfield=label, contents=contents, filename=filename, data=data, key=str(award_keys))
                award_keys+=1.0
            if st.button(f"Remove {award}", help="You may need to refresh using CTRL+R after removing", key=str(award_keys+20.0)): # optional remove work
                del data["awards"][i]
                update_data(filename, data)
    add_awards_prompt(data,filename)

    # Skills
    st.write("#### Skills")
    for i, sc in enumerate(data["skills"]):
        skill_class = str(data["skills"][i]["name"])
        with st.expander(label=skill_class):
            for label in list(sc.keys()):
                contents = data["skills"][i][label]
                if label=="keywords":
                    editable_field(title="", field="skills", subfield=i, subsubfield=label, contents=contents, filename=filename, data=data, key=str(keys), area=True, nolabel=True, tolist=True)
                    # for skill in contents:
                    keys+=0001.0
                else:
                    editable_field(title="skill "+label+"-- *"+skill_class+"*", field="skills", subfield=i, subsubfield=label, contents=contents, filename=filename, data=data, key=str(keys))
                    keys+=0001.0
            if st.button(f"Remove skillset", help="You may need to refresh using CTRL+R after removing", key=str(keys)): # optional remove work
                del data["skills"][i]
                update_data(filename, data)
        keys+=0001.0
    add_skill_prompt(data, filename)

    # Languages
    st.markdown("#### Languages ")
    for i, lang in enumerate(data["languages"]):
        lng = str(data["languages"][i]["language"])
        with st.expander(label=lng):
            editable_field(title="Language", field="languages", subfield=i, subsubfield="lanugage", contents=lng, filename=filename, data=data, key=str(keys))
            keys+=0001.0
            fluency = data["languages"][i]["fluency"]
            if fluency == "Fluent": idx = 0
            elif fluency == "Mastery": idx = 1
            else: idx = 2
            fluency =  st.selectbox(
                "Fluency",
                ("Fluent", "Mastery", "Proficient"), key=str(keys), index=idx)
            keys+=0001.0
            if st.button(f"Remove {lng}", help="You may need to refresh using CTRL+R after removing"): # optional remove work
                del data["lanugages"][i]
                update_data(filename, data)
    add_language_prompt(data, filename)

    col1, col2, col3, col4, col5 = st.columns(5)
    if col3.button("SAVE"):
        update_data(filename, data)



def editable_field(title, field, subfield=None, subsubfield=None, contents="", filename="", data=None, area=False, key=None, autosave=False, nolabel=False, tolist=False):
    """
    Title of editable field
    Data, the actual json
    Field, what we are selecting (i.e: data[name])
    contents: The contents of the thing
    """
    label_visibility = 'visible' if nolabel==False else 'hidden'

    if not area:
        content = st.text_input(label=title, value=contents, key=key, label_visibility=label_visibility)
    else:
        if type(contents) == list:
            strcontents = ""
            for i, item in enumerate(contents):
                if i<len(contents)-1:
                    strcontents+=(str(item))+","
                else:
                    strcontents+=(str(item))
            contents = strcontents
            # st.write(strcontents)
        content = st.text_area(label=title, value=contents, key=key, label_visibility=label_visibility)
    # f = open(filename, "r+")

    # if "," in content or tolist:
    if tolist:
        content = content.split(",")

    if not subsubfield:
        if not subfield:
            data[field] = content # <--- add `id` value.
        else:
            data[field][subfield] = content
    else:
        data[field][subfield][subsubfield] = content

    # if allow_remove:
    #     if st.button(f"Remove {title}"):
    #         del data["work"][subfield]

    if autosave:
        try:
            update_data(filename, data)
        except:
            pass

def update_work():
    pass

def work_add_prompt(data:dict, filename):
    content = st.text_input(label="Add Work Experience?", value="", placeholder="Input Company name here!")
    if st.button(" *Add Experience* "):
        new_work_item = {
                            "company"      : content,
                            "location"     : "",
                            "descriptiom"  : "",
                            "position"     : "",
                            "website"      : "",
                            "startDate"    : "",
                            "endDate"      : "",
                            "summary"      : ""
                        }
        data["work"].append( new_work_item )
        update_data(filename, data)

        st.info("Awesome!, Refresh using CTRL+R to see your updated information")

def add_language_prompt(data:dict, filename):
    lang_keys = 01234.0
    content = st.text_input(label="Add Language", value="", placeholder="Input Language name here!", key=str(lang_keys))
    lang_keys+=00001.0
    if st.button(" *Add Language* "):

        new_language_item = {
                                "language"      : content,
                                "fluency"     : "Proficient",
                            }
        data["languages"].append( new_language_item )
        update_data(filename, data)

        st.info("Awesome!, Refresh using CTRL+R to see your updated information")

def add_skill_prompt(data:dict, filename):
    content = st.text_input(label="Add Skillset", value="", placeholder="Input Skillset name here!")
    if st.button(" *Add Skillset* "):
        new_skillset_item = {
                            "name"      : content,
                            "level"     : "",
                            "keywords"  : list() 
                        }
        data["skills"].append( new_skillset_item )
        update_data(filename, data)

        st.info("Awesome!, Refresh using CTRL+R to see your updated information")

def add_education_prompt(data:dict, filename):
    edu_keys = 02573891234.0
    content = st.text_input(label="Add Education", value="", placeholder="Input Education name here!")
    edu_keys+=00001.0
    if st.button(" *Add Education* "):
        new_education_item = {
                            "institution": content,
                            "area"       : "",
                            "studyType"  : "",
                            "startDate"  : "",
                            "endData"    : "",
                            "gpa"        : "" 
                        }
        data["education"].append( new_education_item )
        update_data(filename, data)

        st.info("Awesome!, Refresh using CTRL+R to see your updated information")


def add_awards_prompt(data:dict, filename):
    awards_keys = 231890578175.0
    content = st.text_input(label="Add Award", value="", placeholder="Input Award name here!")
    awards_keys+=00001.0
    if st.button(" *Add Award* "):
        new_award_item = {
                            "title"    : content,
                            "date"     : "",
                            "awarder"  : "",
                            "summary"  : "" 
                        }
        data["awards"].append( new_award_item )
        update_data(filename, data)

        st.info("Awesome!, Refresh using CTRL+R to see your updated information")


def add_item(title, field, subfield=None, subsubfield=None, contents="", filename="", data=None, area=False):
    pass

def update_data(filename, data):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as jsonFile:
        json_object = json.dumps(data, indent=4)
        # st.write(type(data), type(json_object))
        json.dump(json_object, jsonFile)
    
    # os.remove(filename)
    # db.drive.delete(filename)

    db.drive.put(name=filename, data=json_object)
    
        # Create new file
        


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
            st.info("Warning! Save functionality limited!")
            show_resume(resumejson)
        else:
            st.info("No files to display!")
            st.write("Create one?")
    else:
        st.write("Nothing to display")

if __name__ == "__main__":
    main()
