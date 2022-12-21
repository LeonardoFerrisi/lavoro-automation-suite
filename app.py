import streamlit as st
import streamlit_authenticator as stauth
import database as db

# User application

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
            create_userapplication(userdeta, authenticator)



if __name__ == "__main__":
    a = Application()
    a.main()