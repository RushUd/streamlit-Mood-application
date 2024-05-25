#Modules
import pyrebase
import streamlit as st
from datetime import datetime

#Configuration key
firebaseConfig = {
  'apiKey': "AIzaSyCjJljLRGbo71Q242xVKZcwnTpMbqMp8yU",
  'authDomain': "streamlit-mood-application.firebaseapp.com",
  'projectId': "streamlit-mood-application",
  'databaseURL': "https://streamlit-mood-application-default-rtdb.firebaseio.com",
  'storageBucket': "streamlit-mood-application.appspot.com",
  'messagingSenderId': "199851870438",
  'appId': "1:199851870438:web:5a5f68ca373b64ff4ad327",
  'measurementId': "G-DQBCQ45XYC"
}

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database
db = firebase.database()
storage = firebase.storage()

st.sidebar.markdown("<h1 style='text-align: center;'>Mood Application</h1>", unsafe_allow_html=True)


#Authentication

choice = st.sidebar.selectbox('Login/Sign up', ['Login','Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type = 'password')

if choice == 'Sign up':
  handle = st.sidebar.text_input('Please enter a User Name',value = 'Default')
  submit = st.sidebar.button('Create account')

  if submit:
      user = auth.create_user_with_email_and_password(email,password)
      st.success('Account created successfully!')
      st.balloons()
      #Sign in
      user =  auth.sign_in_with_email_and_password(email,password)
      db.child(user['localId']).child("Handle").set(handle)
      db.child(user['localId']).child("Id").set(user['localId'])
      #Welcome
      st.title('Hello' +" "+ handle)
      st.info('Use login to check back again')

if choice == 'Login':
   login = st.sidebar.checkbox('Login')
   if login: 
      user = auth.sign_in_with_email_and_password(email,password)
      st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

      bio = st.radio('Jump to',['Home','ABC','XYZ'])

      if bio == 'Home':
            st.subheader('Enter your details')
            full_name = st.text_input("Full Name")
            date_of_entry = st.date_input("Date of Entry", datetime.now())
            username = st.text_input("Username", value=user['email'].split('@')[0])
            location = st.text_input("Location")
            submit_details = st.button('Submit')

            if submit_details:
                user_id = user['localId']
                db.child(user_id).child("Full Name").set(full_name)
                db.child(user_id).child("Date of Entry").set(str(date_of_entry))
                db.child(user_id).child("Username").set(username)
                db.child(user_id).child("Location").set(location)
                st.success("Details submitted successfully!")

