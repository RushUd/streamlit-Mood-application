# Modules
import pyrebase
import streamlit as st
from datetime import datetime
import numpy as np
import uuid

# Load CSS
with open("C:/Users/rusha/Downloads/Streamlit/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Configuration key
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

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

st.sidebar.markdown("<h1 style='text-align: center;'>Mood Application</h1>", unsafe_allow_html=True)

# Authentication
choice = st.sidebar.selectbox('Login/Sign up', ['Login', 'Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

if choice == 'Sign up':
    handle = st.sidebar.text_input('Please enter a User Name', value='Default')
    submit = st.sidebar.button('Create account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Account created successfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("Id").set(user['localId'])
        st.title('Hello ' + handle)
        st.info('Use login to check back again')

# Login
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        bio = st.radio('Jump to', ['New Entry', 'History'])

        # New Entry
        if bio == 'New Entry':
            st.subheader('Enter your details')
            full_name = st.text_input("Full Name")
            date_of_entry = st.date_input("Date of Entry", datetime.now())
            username = st.text_input("Username", value=user['email'].split('@')[0])
            location = st.text_input("Location")
            notes = st.text_input("Notes")

            st.subheader('Choose your mood')
            mood_grid = [
                ["Enraged", "Panicked", "Stressed", "Jittery", "Shocked", "Surprised", "Upbeat", "Festive", "Exhilarated", "Ecstatic"],
                ["Livid", "Furious", "Frustrated", "Tense", "Stunned", "Hyper", "Cheerful", "Motivated", "Inspired", "Elated"],
                ["Fuming", "Frightened", "Angry", "Nervous", "Restless", "Energized", "Lively", "Enthusiastic", "Optimistic", "Excited"],
                ["Anxious", "Apprehensive", "Worried", "Irritated", "Annoyed", "Pleased", "Happy", "Focused", "Proud", "Thrilled"],
                ["Repulsed", "Troubled", "Concerned", "Uneasy", "Peeved", "Pleasant", "Joyful", "Hopeful", "Playful", "Blissful"],
                ["Disgusted", "Glum", "Disappointed", "Down", "Apathetic", "At ease", "Easygoing", "Content", "Loving", "Fulfilled"],
                ["Pessimistic", "Morose", "Discouraged", "Sad", "Bored", "Calm", "Secure", "Satisfied", "Grateful", "Touched"],
                ["Alienated", "Miserable", "Lonely", "Disheartened", "Tired", "Relaxed", "Chill", "Restful", "Blessed", "Balanced"],
                ["Despondent", "Depressed", "Sullen", "Exhausted", "Fatigued", "Mellow", "Thoughtful", "Peaceful", "Comfy", "Carefree"],
                ["Despair", "Hopeless", "Desolate", "Spent", "Drained", "Sleepy", "Complacent", "Tranquil", "Cozy", "Serene"]
            ]

            mood_descriptions = [
                ["Overwhelmingly furious and enraged", "Extremely anxious and panicked", "Under significant stress", "Feeling very jittery and on edge", "In shock and disbelief", "Genuinely surprised and startled", "Feeling very positive and upbeat", "In a festive and celebratory mood", "Feeling exhilarated and thrilled", "Experiencing ecstatic joy"],
                ["Deeply angry and livid", "Feeling intense fury", "Highly frustrated and irritated", "Feeling very tense and uneasy", "Completely stunned and speechless", "Incredibly energetic and hyper", "Radiating cheerfulness and joy", "Highly motivated and driven", "Deeply inspired and creative", "Experiencing great elation"],
                ["Seething with anger and fuming", "Extremely scared and frightened", "Feeling intense anger", "Very nervous and apprehensive", "Restless and unable to relax", "Full of energy and vitality", "Feeling lively and spirited", "Highly enthusiastic and eager", "Optimistic and hopeful", "Extremely excited and eager"],
                ["Feeling very anxious and worried", "Apprehensive and cautious", "Overly concerned and worried", "Irritated and annoyed", "Feeling annoyed and bothered", "Pleased and contented", "Experiencing happiness and joy", "Highly focused and attentive", "Feeling proud and accomplished", "Extremely thrilled and excited"],
                ["Repulsed and disgusted", "Feeling troubled and distressed", "Highly concerned and worried", "Uneasy and uncomfortable", "Feeling peeved and annoyed", "Feeling pleasant and agreeable", "Joyful and full of happiness", "Hopeful and optimistic", "Playful and full of fun", "Blissfully happy"],
                ["Disgusted and revolted", "Feeling glum and downcast", "Disappointed and let down", "Feeling down and depressed", "Apathetic and indifferent", "At ease and relaxed", "Easygoing and relaxed", "Content and satisfied", "Feeling loving and affectionate", "Feeling fulfilled and satisfied"],
                ["Pessimistic and negative", "Feeling morose and gloomy", "Discouraged and demotivated", "Sad and unhappy", "Feeling bored and uninterested", "Calm and composed", "Feeling secure and safe", "Satisfied and content", "Grateful and appreciative", "Feeling touched and moved"],
                ["Feeling alienated and isolated", "Miserable and unhappy", "Lonely and desolate", "Disheartened and discouraged", "Feeling tired and exhausted", "Relaxed and at ease", "Chill and laid-back", "Feeling restful and relaxed", "Blessed and fortunate", "Feeling balanced and centered"],
                ["Despondent and hopeless", "Depressed and very sad", "Sullen and withdrawn", "Exhausted and worn out", "Fatigued and tired", "Mellow and calm", "Thoughtful and reflective", "Peaceful and serene", "Feeling comfy and cozy", "Carefree and unworried"],
                ["In despair and hopeless", "Feeling hopeless and desolate", "Desolate and abandoned", "Feeling spent and exhausted", "Drained and depleted", "Sleepy and drowsy", "Feeling complacent and self-satisfied", "Tranquil and calm", "Feeling cozy and comfortable", "Feeling serene and peaceful"]
            ]

            css_classes = [
                ["enraged", "panicked", "stressed", "jittery", "shocked", "surprised", "upbeat", "festive", "exhilarated", "ecstatic"],
                ["livid", "furious", "frustrated", "tense", "stunned", "hyper", "cheerful", "motivated", "inspired", "elated"],
                ["fuming", "frightened", "angry", "nervous", "restless", "energized", "lively", "enthusiastic", "optimistic", "excited"],
                ["anxious", "apprehensive", "worried", "irritated", "annoyed", "pleased", "happy", "focused", "proud", "thrilled"],
                ["repulsed", "troubled", "concerned", "uneasy", "peeved", "pleasant", "joyful", "hopeful", "playful", "blissful"],
                ["disgusted", "glum", "disappointed", "down", "apathetic", "at-ease", "easygoing", "content", "loving", "fulfilled"],
                ["pessimistic", "morose", "discouraged", "sad", "bored", "calm", "secure", "satisfied", "grateful", "touched"],
                ["alienated", "miserable", "lonely", "disheartened", "tired", "relaxed", "chill", "restful", "blessed", "balanced"],
                ["despondent", "depressed", "sullen", "exhausted", "fatigued", "mellow", "thoughtful", "peaceful", "comfy", "carefree"],
                ["despair", "hopeless", "desolate", "spent", "drained", "sleepy", "complacent", "tranquil", "cozy", "serene"]
            ]

            mood_choice = None

            for i, row in enumerate(mood_grid):
                cols = st.columns(10)
                for j, col in enumerate(cols):
                    mood = row[j]
                    css_class = css_classes[i][j]
                    description = mood_descriptions[i][j]
                    button_html = f'<button class="mood-button {css_class}" title="{description}" onclick="window.location.href=\'#{mood}\'">{mood}</button>'
                    col.markdown(button_html, unsafe_allow_html=True)
                    if st.session_state.get(mood):
                        mood_choice = mood
                        st.session_state["mood_choice"] = mood_choice
                        st.session_state["description"] = description


            mood_choice = st.session_state.get("mood_choice", None)
            description = st.session_state.get("description", "")
            
            if mood_choice:
                st.write(f'You selected mood: {mood_choice}')

            submit_details = st.button('Submit')

            if submit_details:
                if not full_name or not location or not notes:
                    st.warning("Please fill out all fields before submitting.")
                else:
                    user_id = user['localId']
                    entry_id = str(uuid.uuid4())  # Generate a unique ID for the entry
                    entry_data = {
                        "Full Name": full_name,
                        "Date of Entry": str(date_of_entry),
                        "Username": username,
                        "Email": email,
                        "Location": location,
                        "Notes": notes,
                        "Mood": mood_choice
                    }
                    db.child("History").child(user_id).child(entry_id).set(entry_data)
                    st.success("Details submitted successfully!")

        # History
        if bio == 'History':
            st.subheader('Your History')

            # Retrieve user ID based on email
            users = db.get().val()
            user_id = None
            for uid, user_data in users.items():
                if user_data.get("Email") == email:
                    user_id = uid
                    break

            if user_id:
                # Retrieve history data based on user ID
                history = db.child("History").child(user_id).get().val()

                if history:
                    for entry_id, entry_data in history.items():
                        st.markdown(f'<div class="history-entry"><h3>Date: {entry_data.get("Date of Entry", "N/A")}</h3>'
                                    f'<p><strong>Location:</strong> {entry_data.get("Location", "N/A")}</p>'
                                    f'<p><strong>Notes:</strong> {entry_data.get("Notes", "N/A")}</p>'
                                    f'<p><strong>Mood:</strong> {entry_data.get("Mood", "N/A")}</p></div>',
                                    unsafe_allow_html=True)
                else:
                    st.info("No history found")
            else:
                st.info("No user found with the given email ID")
