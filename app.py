import streamlit as st
import pandas as pd
import speech_recognition as sr

# Page settings
st.set_page_config(
    page_title="MoodTune Music DJ",
    page_icon="🎵",
    layout="wide"
)

# Black theme
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}

h1,h2,h3,p,label {
    color:white;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
songs = pd.read_csv("songs.csv")

songs.columns = songs.columns.str.lower()

# Mood detection

def detect_emotion(text):

    text = text.lower()

    happy = [
        "happy","good","love",
        "awesome","great",
        "joy","excited"
    ]

    sad = [
        "sad","cry","hurt",
        "lonely","depressed"
    ]

    angry = [
        "angry","hate",
        "annoyed","mad"
    ]

    calm = [
        "peace","calm",
        "relax","spiritual"
    ]

    for w in happy:

        if w in text:

            return "happy"

    for w in sad:

        if w in text:

            return "sad"

    for w in angry:

        if w in text:

            return "angry"

    for w in calm:

        if w in text:

            return "calm"

    return "neutral"


# Recommend songs

def recommend(emotion,
              language,
              category,
              singer):

    rec = songs.copy()

    if emotion != "All":

        rec = rec[
            rec["emotion"]
            .str.lower()
            ==
            emotion.lower()
        ]

    if language != "All":

        rec = rec[
            rec["language"]
            .str.lower()
            ==
            language.lower()
        ]

    if category != "All":

        rec = rec[
            rec["category"]
            .str.lower()
            ==
            category.lower()
        ]

    if singer != "All":

        rec = rec[
            rec["artist"]
            .str.lower()
            ==
            singer.lower()
        ]

    if len(rec)==0:

        return None

    return rec.sample(
        min(10,len(rec))
    )


# Title

st.title("🎵 MoodTune Music DJ")

st.write(
"AI Emotion Based Music Recommendation"
)


# Sidebar

st.sidebar.header("Filters")

language = st.sidebar.selectbox(

    "Language",

    ["All",
     "Hindi",
     "Punjabi",
     "English"]

)

category = st.sidebar.selectbox(

    "Category",

    ["All",

     "party",

     "heartbroken",

     "travel",

     "friendship",

     "qawwali",

     "romantic",

     "motivational",

     "sad"]

)

singer_list = ["All"] + sorted(

    songs["artist"].unique()

)

singer = st.sidebar.selectbox(

    "Singer",

    singer_list

)


# Text Input

st.header("✍️ Text Mood")

text = st.text_input(

    "How are you feeling?"

)

if st.button(

    "Recommend from Text"

):

    emotion = detect_emotion(text)

    st.success(

        f"Detected Mood : {emotion}"

    )

    rec = recommend(

        emotion,

        language,

        category,

        singer

    )

    if rec is not None:

        for _,row in rec.iterrows():

            st.write(

                f"🎵 {row['song']}"

            )

            st.write(

                f"🎤 {row['artist']}"

            )

            st.video(

                row["youtube"]

            )

            st.divider()

    else:

        st.warning(

            "No songs found"

        )


# Voice Input

st.header("🎤 Voice Mood")

audio = st.file_uploader(

    "Upload WAV file",

    type=["wav"]

)

if st.button(

    "Recommend from Voice"

):

    if audio:

        r = sr.Recognizer()

        with sr.AudioFile(audio) as source:

            data = r.record(source)

        text = r.recognize_google(data)

        st.write(

            "Recognized Text:",

            text

        )

        emotion = detect_emotion(text)

        st.success(

            f"Detected Mood : {emotion}"

        )

        rec = recommend(

            emotion,

            language,

            category,

            singer

        )

        if rec is not None:

            for _,row in rec.iterrows():

                st.write(

                    f"🎵 {row['song']}"

                )

                st.write(

                    f"🎤 {row['artist']}"

                )

                st.video(

                    row["youtube"]

                )

                st.divider()

        else:

            st.warning(

                "No songs found"
            )
