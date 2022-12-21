import streamlit as st
import streamlit_authenticator as stauth
import database as db

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

    name = userdata["name"]
    email = userdata["email"]
    password = userdata["password"]
    files = userdata["data"]

    st.markdown(f'# WELCOME! {name}')
    
    if not files:
        st.info(':red[You dont have any data, would you like to create some?]')

        if st.button('Create data'):
            st.info("Excellent! Navigate to the sidebar to your left and select **datamaker**")
        else:
            st.write('Goodbye')

    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.write("Cool Stuff")

def create_userdata(authenticator:stauth.Authenticate):
    with st.sidebar:
        authenticator.logout('Logout', 'main')