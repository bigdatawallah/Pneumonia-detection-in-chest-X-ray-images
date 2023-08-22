import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
import smtplib


auth_key = 'd0wdrf4hnoy_6AZ6t78HKWW8geoy2kBKWfffbC95ZNVE'

# User authentication cedentials
deta = Deta(auth_key)
db = deta.Base('project')

# Patient Data
db2 = deta.Base('patient')


def validate_mobile_number(number):

    pattern = r'^[789]\d{9}$'
    
    if re.match(pattern, number):
        return True
    else:
        return False
    

def validate_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False
    
    # Check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check if the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check if the password contains at least one digit
    if not re.search(r'[0-9]', password):
        return False
    
    # Check if the password contains at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>~]', password):
        return False
    
    return True




def insert_user(email, username,mob, password):

    date_joined = str(datetime.datetime.now())
    
    return db.put({'key': email, 'username': username, 'password': password,"mobile":mob ,'date_joined': date_joined})
    

def fetch_users():

    users = db.fetch()
    return users.items


def get_user_emails():
 
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
   
    pattern = "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    if re.search(r'[A-Z]', username):
        return False
    
    
    if not re.search(r'[a-z]', username):
        return False
    
    
    if not re.search(r'[0-9]', username):
        return False
    
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>~]', username):
        return False
    
    return True
    


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
        mobile = st.text_input(':blue[Mobile]', placeholder='Your Mobile Number')
        

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if validate_password(password1):
                                    if password1 == password2:
                                        if validate_mobile_number(mobile):
                                            
                                            hashed_password = stauth.Hasher([password2]).generate()
                                            insert_user(email, username, mobile,hashed_password[0])         # Add User to DB
                                            st.success('Account created successfully!!')
                                            st.balloons()
                                        else:
                                            st.warning("Mobile number is not valid")
                                    else:
                                        st.warning('Passwords Do Not Match')
                                else:
                                    st.warning('Password is not valid. Should be like "Xyz@123"')
                            else:
                                st.warning('Username Too short')
                        else:
                            st.warning('Username Already Exists')
                    else:
                        st.warning('Invalid Username!Should only Contain smallcase and numbers.')
                else:
                    st.warning('Email Already exists!!')
            else:
                st.warning('Invalid Email')

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)
        
        with btn3:
            st.form_submit_button('Sign Up')


def validate_age(age):
    try:
        age = int(age)
        if age > 0 and age < 120:
            return True
        else:
            return False
    except:
        pass

def patient_info(name,age,mob):

    if validate_age(age):

        if validate_mobile_number(mob):
        
            date_joined = str(datetime.datetime.now())
            db2.put({"name":name,"age":age,"mobile":mob,"Date_joined":date_joined})
            st.balloons()

        else:
            st.warning("Mobile number is not valid")
    else:
        
        st.warning("Age is not valid")

def patient_form():

   with st.form(key="patient_info",clear_on_submit=True):
      st.subheader(':green[Patient Details]')
      name = st.text_input("Enter patient's name")
      age = st.text_input("Enter patient's age")
      mob = st.text_input("Enter patient's Mobile")
      if st.form_submit_button(":green[Submit]"):
          patient_info(name,age,mob)

def change_pass(new_pass):
    st.success("Password has been updated")


def send_otp(email):

    try:
        HOST = "smtp.googlemail.com"
        PORT = 587

        FROM_EMAIL = "pandey.sp.shiva625@gmail.com"

        TO_EMAIL = email
        PASSWORD = "jmauqsioloeueqjb"


        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        MESSAGE = """Subject: Pneumonia Detection Website
    This is your otp 56456 to reset your password..."""

        smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)

        smtp.quit()
        return True
    except:
        return False

def forgot_pass():


    o = False
    with st.form(key="Forgot Password",clear_on_submit=True):
        st.subheader(':red[Reset your password]')
        email = st.text_input("Enter your email",placeholder="Otp will be send to provided email")
        if st.form_submit_button("send otp"):
            if validate_email(email):
                if send_otp(email):
                    st.success("OTP sent to your email")
                    o = True
                else:
                    st.warning("OTP sent to your email")
            else:
                st.warning('Wrong email !!!')
        if o:     
            st.checkbox("confirm")
            opt = st.text_input("Enter your OTP")
            new_pass = st.text_input("Enter new passeord")
            confirm_pass = st.text_input("Confirm new passeord")
            
            if st.form_submit_button(":green[Change]"):
                st.success("Password has been updated")
                change_pass(new_pass)

                    


