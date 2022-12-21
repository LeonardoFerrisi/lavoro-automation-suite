import streamlit as st
import streamlit_authenticator as stauth
import database as db
import userapplication as userapp
from userapplication import change_state, check_state, log_user, unlog_user

class Application:

    def __init__(self):
        self.LOGGEDIN = False
        self.current_user = None

    def prompt_registration(self, authenticator:stauth.Authenticate, credentials, preauthorization=False):

        current_usernames = credentials["usernames"].keys()
        try:
            if authenticator.register_user(form_name='Register user', location="main", preauthorization=False):
                db.update_all(credentials)
                st.success('User registered successfully')
                self.prompt_login(authenticator, credentials)
        except Exception as e:
            st.error(e)

    def prompt_login(self, authenticator:stauth.Authenticate, credentials):
        
        if check_state():
            change_state("False")
            unlog_user()
            
        # Show Login Form
        name, authentication_status, username = authenticator.login("Login", "main")
        if authentication_status == False:
            st.error("Username/password is incorrect")
        if authentication_status == None:
            st.warning("Please enter your username and password")
        if authentication_status:
            st.write("Success!")
            log_user(username=username)
            

            # userdeta = credentials["usernames"][username]
            self.current_user = username
            # Have a logout button on sidebar
            self.LOGGEDIN = True
            change_state("True")

    def main(self):
        
        self.LOGGEDIN = False

        st.set_page_config(page_title="Applicant Tuner", page_icon=":bar_chart:", layout="wide")
        st.title("Applicant Tuner")
        st.subheader("WebApp for tuning your information to whatever Job you apply for")

        # Prompt user to sign in


        # --- DEMO PURPOSE ONLY --- #
        # placeholder = st.empty()
        # placeholder.info("CREDENTIALS | username:pparker ; password:abc123")
        # ------------------------- #
        
        # --- USER AUTHENTICATION ---
        users = db.fetch_all_users()
        print(users)
        usernames = [user["key"] for user in users]
        names = [user["name"] for user in users]
        emails = [user["email"] for user in users]
        hashed_passwords = [user["password"] for user in users]

        credentials = {"usernames":{}}

        for user in users:
            user_data = {
                            "name"    : user["name"],
                            "email"   : user["email"],
                            "password": user["password"],
                            "data"    : user["data"]
                        }
                            
            credentials["usernames"][user["key"]] = user_data

        authenticator = stauth.Authenticate(credentials=credentials, cookie_name="sales", key="abcdef", cookie_expiry_days=30, preauthorized=["default@gmail.com"])

        self.AUTH = authenticator

        # if st.button("Register"):
        #     prompt_registration(authenticator=authenticator)

        # if st.button("Login"):
        #     prompt_login(credentials, authenticator)
        self.prompt_login(authenticator, credentials)

        # with st.sidebar:
        #     actions = {
        #         "Login"   : self.prompt_login,
        #         "Register": self.prompt_registration
        #     }

        #     using = st.selectbox("Choose an action", actions.keys())

        #     actions[using](authenticator, credentials)
        
        if self.LOGGEDIN:
            userdeta = credentials["usernames"][self.current_user]
            userapp.create_userapplication(userdeta, authenticator)



if __name__ == "__main__":
    a = Application()
    a.main()