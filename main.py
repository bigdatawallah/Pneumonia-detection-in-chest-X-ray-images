import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users






st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')

st.markdown('''

            <style> .css-zq5wmm.ezrtsby0 {visibility:hidden;}</style>
            <style> .css-cio0dv.ea3mdgi1 {visibility:hidden;}</style>

''',unsafe_allow_html=True)

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    
    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        inp = st.sidebar.radio("Create an Account",["Login",'Signup'])

        if inp == 'Signup':
            sign_up()
            

           

    if username:
        if username in usernames:
            if authentication_status:
                st.balloons()
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.subheader('Pneumonia Detection Website')
                st.markdown(
                    """
                    # Welcome To CDAC
                    
                    """
                )

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    st.success('Refresh Page')
