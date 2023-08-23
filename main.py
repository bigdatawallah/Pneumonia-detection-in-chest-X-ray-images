import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users,patient_form,forgot_pass,reset_pass






st.set_page_config(page_title='Pneumonia Detection', page_icon="chart_with_upwards_trend", initial_sidebar_state='auto')

st.markdown('''

            <style> .css-zq5wmm.ezrtsby0 {visibility:hidden;}</style>
            <style> .css-cio0dv.ea3mdgi1 {visibility:hidden;}</style>

''',unsafe_allow_html=True)





# try:
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


email, authentication_status, username = Authenticator.login(':green[Login]', 'sidebar')



info, info1 = st.columns(2)


        

if username:
    if username in usernames:
        if authentication_status:

            
            st.sidebar.subheader(f'Welcome {username}')

            Authenticator.logout(':red[Log Out]', 'sidebar')

            

            st.subheader(':red[Pneumonia Detection Website]')

            patient_form()


        elif not authentication_status:
            with info:
                st.sidebar.error('Incorrect Password or username')
        else:
            with info:
                st.sidebar.warning('Please feed in your credentials')
    else:
        with info:
            st.sidebar.warning('Username does not exist, Please Sign up')
inp = None  
if not authentication_status:
    inp = st.sidebar.radio("Select Option",['SIGN UP',"RESET PASSWORD","FORGOT PASSWORD"])

if inp == 'SIGN UP':
    sign_up()
elif inp == 'FORGOT PASSWORD':
    forgot_pass()
elif inp == 'RESET PASSWORD':
    reset_pass()


# except:
#     st.success('Refresh Page')
