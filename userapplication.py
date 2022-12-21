import streamlit as st
import streamlit_authenticator as stauth
import database as db

def change_state(state="False"):
    with open('pages/state.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    data[0] = f'{state}\n'
    with open('pages/state.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)

def check_state():
    with open('pages/state.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    if data[0] == "True" or data[0] == "True\n":
        return True
    else: return False

def check_usr():
    with open('pages/state.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    return data[1]

def log_user(username):
    with open('pages/state.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    usr = data[1]
    if usr != username and usr != f"{username}\n":
        data[1] = f'{username}\n'
        with open('pages/state.txt', 'w', encoding='utf-8') as file:
            file.writelines(data)

def unlog_user():
    with open('pages/state.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    usr = data[1]
    if usr != "null" and usr != "null\n":
        data[1] = "null\n"
        with open('pages/state.txt', 'w', encoding='utf-8') as file:
            file.writelines(data)

def create_userapplication(userdata, authenticator:stauth.Authenticate):
    """
    userdata is formatted as follows:

    {   username : {
                        "name"    : user["name"],
                        "email"   : user["email"],
                        "password": user["password"],
                        "data"    : user["data"]
                    }
    }
    """

    # st.set_page_config(
    #     page_title="Applicant Tuner: Main",
    #     page_icon="👋",
    # ) 

    change_state(state="True")
    
    name = userdata["name"]
    email = userdata["email"]
    password = userdata["password"]
    files = userdata["data"]    

    st.markdown(f'# WELCOME! {name}')
    
    if not files:
        st.info(':red[You dont have any data, would you like to create some?]')

        if st.button('Create data'):
            st.info("Excellent! Navigate to the sidebar to your left and select **your info**")
        else:
            st.write('Goodbye')

    with st.sidebar:
        authenticator.logout('Logout', 'main')

def create_userdata(authenticator:stauth.Authenticate):
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        