import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users,patient_form,forgot_pass,reset_pass ,load_lottie,save_image,predict
from streamlit_lottie import st_lottie

st.set_page_config(page_title='Pneumonia Diagnosis', page_icon=":hospital:", initial_sidebar_state='collapsed')



st.markdown('''
            

             <style> .css-z3au9t.ea3mdgi2 {visibility:hidden;}</style>
             <style> .css-cio0dv.ea3mdgi1 {visibility:hidden;}</style>
             <style> .css-zq5wmm.ezrtsby0 {visibility:hidden;}</style>

            <style> .css-aw8l5d.eczjsme1 {color: rgb(40 255 47);top: 0.5rem;}</style>
            <style> .css-1avcm0n.ezrtsby2 {height: 0.875rem;}</style>
        
            <style> .css-1b9x38r.eczjsme2 {color: rgb(500 87 94);top: 0.5rem;}</style>
            <style> .css-1544g2n.eczjsme4 {padding: 10rem 1rem 45.5rem;}</style>
            <style> .css-fblp2m {width: 3.25rem;height: 3.25rem;}</style>
            <style> .css-zt5igj.e1nzilvr3 {text-align: center;}</style>
            <style> .css-10trblm.e1nzilvr0 {font-size:45px;}</style>
           
            

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


email, authentication_status, username = Authenticator.login(':green[Login]', 'main')


if username:
    if username in usernames:
        if authentication_status:
                
                st.title(':stethoscope: :red[Pneumonia Scan] :stethoscope:')
                

                with st.sidebar:
                    
                    
                    st.subheader(f':house_with_garden: Welcome :green[{username}]')
                    Authenticator.logout(':red[Log Out]', 'sidebar')
                
                    lottie = load_lottie("lottie_images\hello.json")
                    st_lottie(lottie,quality="high",height=200)
                    
                        

                
                lottie = load_lottie("lottie_images\lung.json")
                st_lottie(lottie,quality="high",height=200)
            
            

                status,img = patient_form(username)
                if status:
                    p_status,prediction = predict(img)
                    if p_status:
                        if prediction == 'Pneumonia':
                            st.title(":cold_sweat: You are diagnosed with 'Pneumonia'")
                        else:
                            st.balloons()
                            st.title(":slightly_smiling_face: Your test result is 'Normal'")
                
                    
                    



        else:
                st.error('Incorrect username or Password !')
    else:
            st.error('Incorrect username or Password !')

if not authentication_status:
    with st.sidebar:
        st.markdown("""<h1><span style='color:#87CEEB'>Option Menu</span></h1>""", 
            unsafe_allow_html=True,)
        inp = st.selectbox(label="hjgh",options=['SIGN UP',"RESET PASSWORD","FORGOT PASSWORD"],label_visibility="hidden")

        if inp == 'SIGN UP':
            sign_up()
        elif inp == 'FORGOT PASSWORD':
            forgot_pass()
        elif inp == 'RESET PASSWORD':
            reset_pass()


# except:
#     st.success('Refresh Page')
