import streamlit as st
import streamlit_authenticator as stauth
import datetime,numpy as np
import re,os
from deta import Deta     #No sql free cloud based database "link ---> https://deta.space/" 
import smtplib
import random
import string
import bcrypt
import json
import tensorflow as tf
import cv2

# Database authentication cedentials

auth_key = 'Your authentication key'
deta = Deta(auth_key)
db = deta.Base('your base name')

# Patient Database
db2 = deta.Base('Your base name')


def validate_mobile_number(number):
# Check if mobile number is in correct format or not (indian mobile number)
    pattern = r'^[6789]\d{9}$'
    
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

def generate_random_password(length=8):        
    characters = string.ascii_letters + string.digits + string.punctuation        # Generating random password which will be used for reseting users passowrd
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def validate_email(email):
                                       
    pattern = "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"        # Checking if email is in correct format or not

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    if re.search(r'[A-Z]', username):
        return False
                                                        # Checking if username is only containing small cases and numbers 
    
    if not re.search(r'[a-z]', username):
        return False
    
    
    if not re.search(r'[0-9]', username):
        return False
    
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>~]', username):
        return False
    
    return True
    
def validate_age(age):
    try:
        age = int(age)
        if age > 0 and age < 120:         # validating correct age
            return True
        else:
            return False
    except:
        pass


def insert_user(email, username,mob, password):
                                                        # Inserting user signup credentials in database
    date_joined = str(datetime.datetime.now())
    
    return db.put({'key': email, 'username': username, 'password': password,"mobile":mob ,'date_joined': date_joined})
    

def fetch_users():

    users = db.fetch()        # reading all user information from database
    return users.items


def get_user_emails():

    users = db.fetch()        # reading emails of all users from database and appending them in a list and returning the list
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    
    users = db.fetch()
    usernames = []
    for user in users.items:                    # reading usernames of all users from database and appending them in a list and returning the list
        usernames.append(user['username'])
    print(usernames)
    return usernames


def get_password(email):
    p = None
    users = db.fetch()
    for user in users.items:                    # reading hashed passowrds of desired user from database and returning it
        if user['key'] == email:
            p = user['password']
            break
    return p
    


def sign_up():
    with st.sidebar.form(key='signup', clear_on_submit=True):
        st.markdown("""<h3><span style='color:violet'>SIGN UP</span></h3>""", 
               unsafe_allow_html=True,)
        email = st.text_input(label=':email: :blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(label=':id: :blue[Username]', placeholder='Enter Your Username')                           # Signup form 
        mobile = st.text_input(label=':vibration_mode: :blue[Mobile]', placeholder='Your Mobile Number')
        password1 = st.text_input(label=':lock: :blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(label=':lock: :blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
        
        if st.form_submit_button(label='Sign Up'):
        

            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 2:                                                # All the validation to prevent false entries
                                    if validate_password(password1):
                                        if password1 == password2:
                                            if validate_mobile_number(mobile):
                                                
                                                hashed =  stauth.Hasher([password1]).generate()        # Converting the user's password into hashed password
                                                insert_user(email, username, mobile,hashed[0])         # Adding User to Database
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
                                st.warning('Username Already Exists')                                        # Showing warnings for false input
                        else:
                            st.warning('Invalid Username!Should only Contain smallcase and numbers.')
                    else:
                        st.warning('Email Already exists!!')
                else:
                    st.warning('Invalid Email')
            else:
                st.warning('Invalid Email')



def patient_info(username,name,age,mob,image):
    if name:
        if validate_age(age):
                                                                                    # Validation to prevent false entries
            if validate_mobile_number(mob):
            
                date_joined = str(datetime.datetime.now())
                db2.put({"Username":username,"Patient Name":name,"Age":age,"Mobile":mob,"Date joined":date_joined,"Image":image})        # Inserting patient information into database
                return True                                                                                                        # This data can be used for future analysis

            else:                                                                                    
                st.warning("Mobile number is not valid")
        else:
            
            st.warning("Age is not valid")
    else:
        st.warning("Invalid Patient Name...")
    return False


def patient_form(username):
    with st.form(key="patient_info",clear_on_submit=False):
        st.subheader(':green[Patient Details]')
        name = st.text_input(label="Enter patient's name")                            # Patient form to take input like --> name,age,mobile,image of x-ray
        age = st.text_input(label="Enter patient's age")
        mob = st.text_input(label="Enter patient's Mobile")
        img = st.file_uploader(label="Upload Pneumonia X-ray Image", type=["jpg", "png",])

        if st.form_submit_button(label=":green[Submit]"):
            if img is not None:
                d = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")  # Replacing colons with underscores
                image_name = f"{username}_{d}_{img.name}"
                if patient_info(username,name,age,mob,image_name):
                    save_image(img,username,image_name)
                    return True,image_name
        return False,False

def send_pass(email,new_pass):

    try:
        HOST = "smtp.googlemail.com"
        PORT = 587

        FROM_EMAIL = "write email from which you want to send email"

        TO_EMAIL = email
        PASSWORD = "Password to connect to email"
                                                                    # This function is used to send new reseted password on user's provided email.

        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        

        MESSAGE = """Subject: Pneumonia Detection Website \n\n
    your new password is '{}' """.format(new_pass)

        smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)

        smtp.quit()
        return True
    except:
        pass

def set_pass(email,new_pass = generate_random_password()):
    try:
        users = db.fetch()
        for user in users.items:
            if user['key'] == email:
                hashed = stauth.Hasher([new_pass]).generate()            # Setting new pass for desired user in database
                db.update(key=email,updates={'password':hashed[0]})
                return new_pass
    except:
        st.success("Refresh and try again....")    
    
def reset_pass():
    with st.sidebar.form(key="Reset Password",clear_on_submit=True):
            st.markdown("""<h3><span style='color:orange'>CHANGE PASSWORD</span></h3>""",         # Passowrd reset form to set new password
               unsafe_allow_html=True,)
            email = st.text_input(label=":email: :green[Email]",placeholder="Enter Your Current Email")
            curr_pass = st.text_input(label=":lock: :green[Current Passowrd]",placeholder="Enter Your Current Passowrd",type='password')
            new_passs = st.text_input(label=":lock: :green[New Password]",placeholder="Enter Your New Passowrd",type='password')
            confirm_new_passs = st.text_input(label=":lock: :green[Confirm New Password]",placeholder="Confirm Your New Password",type='password')
            
            if st.form_submit_button(label=':green[Change]'):

                if validate_email(email):
                    if email in get_user_emails():
                        if validate_password(new_passs):
                            if new_passs == confirm_new_passs:
                                if bcrypt.checkpw(curr_pass.encode(), get_password(email).encode()):        # checking if current password is matching with provided current passowrd
                                    
                                    
                                    new_pass = set_pass(email,new_passs) 
                                    if send_pass(email,new_pass):
                                        
                                        
                                        st.success("Passowrd Changed Succesfully. Login Please..",icon="✅")

                                        
                                    else:
                                        st.warning("OTP sent to your email")
                                else:
                                    st.warning("Wrong Password !!!")
                            else:
                                st.warning("Password not matching !!!")
                        else:
                            st.warning('New password is not valid. Should in format "Xyz@123"')
                    else:
                        st.error("Email not found !!!")
                else:
                    st.warning('Wrong email !!!')

def forgot_pass():
        
        with st.sidebar.form(key="Forgot Password",clear_on_submit=True):
            st.markdown("""<h3><span style='color:red'>GET NEW PASSWORD</span></h3>""", 
               unsafe_allow_html=True,)                        
            email = st.text_input(label=':email: :green[Email]',placeholder="Password will be send to provided email")
            
            if st.form_submit_button(label=':red[Send]'):
                if email:
                    if validate_email(email):
                        if email in get_user_emails():        
                            new_pass = set_pass(email)           # reseting password and setting new random generated password for user
                            
                            if send_pass(email,new_pass):        # sending that new password to user on his provided email if it exists.
                                
                                
                                st.success("Passowrd sent to your email. Login or Change it.",icon="✅")

                                
                            else:
                                st.warning("OTP sent to your email")
                        else:
                            st.error("Email not found !!!")
                    else:
                        st.warning('Email not found !!!')
                else:
                    st.warning("Please enter email...")

def load_lottie(path:str):

    with open(path,"r") as f:            # Animation related function
        return json.load(f)
    

def save_image(uploaded_file, username,image_name):
    if uploaded_file is not None:                        # Saving actual image file in seprate folder
        image_folder = "patient_images" 
        
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Image Loaded successfully!")

def PneumoniaPrediction(img,model):
    img = np.array(img)/255
    img = img.reshape(1,200, 200, -1)
    isPneumonic = model.predict(img)            # This function is used to make prediction with provided model and image
    print(isPneumonic)
    
    if isPneumonic[0][0] >=0.5:
        imgClass = "Pneumonia"
    else:
        imgClass = "Normal"
    return imgClass


def img_process_V2(img):
    img_size = 200
    img_arr = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    resized_arr = cv2.resize(img_arr, (img_size, img_size))        # This function is working for processing image into desired array for prediction
    return resized_arr

def predict(image_name):
    model = tf.keras.models.load_model("model.h5")                # Loading model
    
    image_folder = "patient_images"                                 
    image_path = os.path.join(image_folder, image_name)            # Loading image 

    image=img_process_V2(image_path)                               # Processed the image into required array format
    ans=PneumoniaPrediction(image,model)                           # Finally Making Prediction     

    return True,ans
    