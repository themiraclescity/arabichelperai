import streamlit as st
import time
import numpy as np
#import pyautogui
import os
#import psutil
import pandas as pd
#import speech_recognition as sr
#from gtts import gTTS
from openai import OpenAI
#from dotenv import load_dotenv
from streamlit_TTS import text_to_speech, text_to_audio, auto_play
from pathlib import Path


api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key missing in")


#Page config
st.set_page_config(page_title="Arabic AI Tutor",page_icon="📚",layout="centered")
#st.image("/static/cat.jpg", caption="Sunrise by the mountains")
st.sidebar.success("Select a demo above.")

mode = st.selectbox(
    "اختر نوع التحليل:",
    [
        "تصحيح إملائي فقط",
        "تصحيح نحوي فقط",
        "تشكيل الكلمات فقط",
        "أعراب فقط",
        "تحليل كامل (إملاء + نحو + تشكيل + إعراب)"
    ]
)
if mode == "تصحيح إملائي فقط":
    system_prompt = """
أنت مدقق إملائي عربي.
صحح الأخطاء الإملائية فقط دون شرح طويل.
"""
elif mode == "تصحيح نحوي فقط":
    system_prompt = """
أنت معلم نحو عربي.
صحح الأخطاء النحوية واشرحها.
"""
elif mode == "تشكيل الكلمات فقط":
    system_prompt = """
             أنت معلم لغة عربية خبير في:
            - الإملاء
            - النحو
            - الإعراب
            - التشكيل

            قم بالخطوات التالية بالترتيب:

            1. اكتشف الأخطاء الإملائية وصححها
            2. صحح الأخطاء النحوية
            3. أعد كتابة الجملة مع التشكيل الكامل

            استخدم التنسيق التالي:

            📝 الجملة بعد التصحيح الإملائي والنحوي والتشكيل:
            (الجملة النهائية مشكولة)

            """
elif mode == "أعراب فقط":
    system_prompt = """
             أنت معلم لغة عربية خبير في:
            - الإملاء
            - النحو
            - الإعراب
            - التشكيل

            قم بالخطوات التالية بالترتيب:

            1. اكتشف الأخطاء الإملائية وصححها
            2. صحح الأخطاء النحوية
            3. أعد كتابة الجملة مع التشكيل الكامل
            4. قم بإعراب كل كلمة

            استخدم التنسيق التالي:

            📝 الجملة بعد التصحيح الإملائي والنحوي والتشكيل:
            (الجملة النهائية مشكولة)

            📘 الإعراب:
            (إعراب كل كلمة)
            """
else:
    system_prompt = """
             أنت معلم لغة عربية خبير في:
            - الإملاء
            - النحو
            - الإعراب
            - التشكيل

            قم بالخطوات التالية بالترتيب:

            1. اكتشف الأخطاء الإملائية وصححها
            2. صحح الأخطاء النحوية
            3. أعد كتابة الجملة مع التشكيل الكامل
            4. قم بإعراب كل كلمة
            5. اشرح بشكل مبسط
            6. حدد نوع الجملة

            استخدم التنسيق التالي:

            📝 الجملة بعد التصحيح الإملائي والنحوي والتشكيل:
            (الجملة النهائية مشكولة)

            🧩 التصحيح الإملائي:
            (اذكر الأخطاء الإملائية فقط إن وجدت)

            📘 الإعراب:
            (إعراب كل كلمة)

            📘 الشرح:
            (شرح مبسط)

            🧾 نوع الجملة:
            """
user_input = st.text_area("Enter Arabic sentence:", placeholder="ذهبت الولد الى المدرسة", value="ذهبت الولد الى المدرسة",)

if st.button("حلل"):
    if user_input:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":system_prompt
                },
                {"role": "user", "content": user_input}
            ]
        )

        #st.write(response.choices[0].message.content)
        st.markdown("### ✨ نتيجة التحليل:")
        result = response.choices[0].message.content
        if "📝" in result:
            sections = result.split("\n")
            for section in sections:
                if "📝" in section:
                    st.success(section)
                elif "🧩" in section:
                    st.warning(section)
                elif "📘" in section:
                    st.info(section)
                else:
                    st.write(section)
        else:
            st.write(result)


# exit_app_button = st.button("Shut Down Browser and App")
# if exit_app_button:
    # st.warning("Closing the browser tab and terminating the app in 5 seconds...")
    # time.sleep(5)  # Give user time to see the message
    # # Simulate Ctrl+W (close tab)
    # pyautogui.hotkey('ctrl', 'w')
    # # Optionally, terminate the Python process as well
    # pid = os.getpid()
    # p = psutil.Process(pid)
    # p.terminate()

st.markdown(""" +++مساعد الاعراب+++ """)
st.button("Re-run")

#linke
#https://pypi.org/project/streamlit-TTS/

model = st.selectbox(
    "Model",
    [
        "gpt-4o-mini-tts",  # newest TTS model
        "tts-1",
        "tts-1-hd",
    ],
    index=0,
)

voice = st.selectbox(
    "Voice",
    [
        "alloy",
        "ash",
        "ballad",
        "coral",
        "echo",
        "fable",
        "nova",
        "onyx",
        "sage",
        "shimmer",
        "verse",
        "marin",
        "cedar",
    ],
    index=0,
)

response_format = st.selectbox(
    "Audio format",
    ["mp3", "wav", "aac", "flac", "opus"],
    index=0,
)

instructions = st.text_area(
    "Optional speaking instructions",
    value="Speak in a clear, natural tone.",
    help="You can guide style, tone, speed, etc.",
)

# ---- Main input ----
default_text = "Today is a wonderful day to build something people love!"
text = st.text_area(
    "Text to convert to speech",
    value=default_text,
    height=150,
)

generate_button = st.button("Generate speech")

# ---- TTS generation ----
if generate_button:
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Generating audio..."):
            # Call OpenAI TTS endpoint
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format=response_format,
                instructions=instructions if instructions.strip() else None,
            )

            # response is bytes-like for audio
            audio_bytes = response.read()
            st.success("Audio generated!")
            # Play audio in the browser
            st.audio(audio_bytes, format=f"audio/{response_format}")
            st.write("Audio size:", len(audio_bytes))
            # Save to disk
            temp_path = f"speech.{response_format}"
            response.write_to_file(temp_path)

            # Read file back into Streamlit
            with open(temp_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format=f"audio/{response_format}", autoplay=True)
            st.write(temp_path)

        # Download button
        st.download_button(
            label="Download audio",
            data=audio_bytes,
            file_name=f"speech.{response_format}",
            mime=f"audio/{response_format}",
        )

st.markdown(
    """
---
**Note:** The voice you hear is AI‑generated using OpenAI's text‑to‑speech API.
"""
)
