import streamlit as st
from audiorecorder import audiorecorder
import openai
import os

# Check if the API key is present in the environment variables
if "OPENAI_API_KEY" not in os.environ:
    # If not present, set it to a default value
    os.environ["OPENAI_API_KEY"] = "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"

# Set the API key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0)
    return response.choices[0].message["content"]


def transcribe(audio_path):
    audio_file = open(audio_path, "rb")
    transcript = openai.Audio.translate_raw("whisper-1", audio_file, filename = '1.mp3')
    return transcript["text"]


def get_ddx(vignette):
    messages_ddx = [
        {'role': 'system', 'content': 'You are a Physician AI assistant tool. Write a differential diagnosis for a patient. Write just diagnoses and justification. Do no write any additional information. Do not write any introduction.'},
        {'role': 'user', 'content': vignette}]
    ddx = get_completion(messages_ddx)
    return ddx


def get_orders(vignette, ddx):
    messages_orders = [
        {'role': 'system', 'content': 'You are a Physician AI assistant tool. Write an order set for a patient to differentiate between conditions. Write just orders and justification. Do no write any additional information. Do not write any introduction.'},
        {'role': 'user', 'content': f'Information about patient: {vignette}. Differential diagnosis: {ddx}'}]
    orders = get_completion(messages_orders)
    return orders


if 'vignette' not in st.session_state:
    st.session_state['vignette'] = ''

if 'ddx' not in st.session_state:
    st.session_state['ddx'] = ''

if 'orders' not in st.session_state:
    st.session_state['orders'] = ''

if 'length' not in st.session_state:
    st.session_state['length'] = 0


st.title("HealthCare-Differential-Diagnosis-DDx")
st.markdown(
    "Record your patient presentation and get the differential diagnoses and orders.")
st.divider()

audio = audiorecorder("Record", "Stop")


if (len(audio) != st.session_state['length']):
    st.session_state['length'] = len(audio)
    # wav_file = open("audio.mp3", "wb")
    # wav_file.write(audio.tobytes())
    transcript = openai.Audio.translate_raw("whisper-1", audio.tobytes(), filename = '1.mp3')
    transcript["text"]
    st.session_state['vignette'] += transcript["text"]


st.session_state['vignette'] = st.text_area(
    "Matches", value=st.session_state['vignette'])


if st.button("Get DDX and Orders"):
    vignette = st.session_state['vignette']
    ddx = get_ddx(vignette)
    st.session_state['ddx'] = ddx
    st.session_state['orders'] = get_orders(vignette, ddx)


col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"**DDX**\n\n{st.session_state['ddx']}", unsafe_allow_html=True)

with col2:
    st.markdown(
        f"**ORDERS**\n\n{st.session_state['orders']}", unsafe_allow_html=True)
