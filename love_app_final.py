import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Fundal roz pastel + text închis
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffc0cb;
        color: #330033;
    }
    /* Override pentru componente cu fundal implicit alb */
    .css-1d391kg, .css-1offfwp, .css-1v3fvcr {
        background-color: rgba(255, 192, 203, 0.6) !important;
        color: #330033 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titlu și GIF drăguț
st.title("💗 How Are You Today, My Love?")
st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", width=200)
st.markdown("Tell me honestly... 🥹")

# Inputs
name = st.text_input("What's your name today? 😄")
now = datetime.now().strftime("%Y-%m-%d %H:%M")

st.divider()

col1, col2 = st.columns(2)

with col1:
    love = st.slider("How loved do you feel? 💞", 0, 10, 5)
    energy = st.slider("How much energy do you have? ⚡", 0, 10, 5)
    missing = st.slider("How much do you miss me? 😘", 0, 10, 5)

with col2:
    peace = st.slider("How calm do you feel? ☁️", 0, 10, 5)
    cuddly = st.slider("How cuddly are you feeling? 🐻", 0, 10, 5)
    sleep = st.slider("How many hours did you sleep? 💤", 0, 12, 7)

# Calcul scor
def calculate_score(love, energy, missing, peace, cuddly):
    score = love * 2 + peace + cuddly + energy - missing // 2
    return max(0, min(100, score))

# Salvează date
def save_data(name, score, sleep, timestamp):
    new_data = pd.DataFrame({
        "Name": [name],
        "HeartScore": [score],
        "Sleep": [sleep],
        "Timestamp": [timestamp]
    })

    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv")
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_csv("mood_log.csv", index=False)

# Afișează rezultat la apăsarea butonului
if st.button("💌 Send Me Your Mood"):
    score = calculate_score(love, energy, missing, peace, cuddly)

    st.subheader("💓 Your Heart Score:")
    st.metric("Heart Score Today", f"{score}/100")

    if score >= 80:
        st.success("You're in the clouds! I want to hug you right now! 🌈")
    elif score >= 50:
        st.warning("You're doing okay. Sending you a kiss to make it better 💋")
    else:
        st.error("I’m worried about you... Sending a big warm hug 🫂")

    save_data(name, score, sleep, now)

# Grafice
if os.path.exists("mood_log.csv"):
    df = pd.read_csv("mood_log.csv")

    st.subheader("📊 Your Mood Over Time:")
    fig, ax = plt.subplots()
    ax.hist(df["HeartScore"], bins=10, color="lightcoral", edgecolor="black")
    ax.set_title("Heart Score Distribution")
    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Days")
    st.pyplot(fig)

    st.subheader("😴 Sleep Hours")
    fig2, ax2 = plt.subplots()
    ax2.hist(df["Sleep"], bins=range(0, 13), color="#92c9e0", edgecolor="black")
    ax2.set_title("Your Sleep Pattern")
    ax2.set_xlabel("Hours")
    ax2.set_ylabel("Number of Days")
    st.pyplot(fig2)

# Mesaj final de dragoste la apăsarea OK
st.markdown("---")
if st.button("✅ OK"):
    st.balloons()
    st.success("I love you, iuba duba 💕 You're the best boyfriend 💘")
