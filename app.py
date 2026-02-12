import streamlit as st
from app.main import MusicLLm
from app.utils import *
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI Music Composer",layout="centered")
st.title("AI Music Composer")
st.markdown("Generate AI music by describing the style and content")

music_input=st.text_input("Describe the music you want to compose!")
style=st.selectbox("Choose a style",["Sad","Happy","Rock","Jazz","Romantic","Extreme"])

if st.button("Generate music") and music_input:
    generator=MusicLLm()
    with st.spinner("Generating music"):
        melody=generator.generate_melody(music_input)
        harmony=generator.generate_harmony(melody)
        rythm=generator.generate_rythm(melody)
        composition=generator.adapt_style(style,melody,harmony,rythm)
        
        melody_notes=melody.split()
        melody_freqs=note_to_frequencies(melody_notes)
        
        harmony_chords=harmony.split()
        harmony_notes=[]
        for chord in harmony_chords:
            harmony_notes.extend(chord.split('-'))
        harmony_freqs=note_to_frequencies(harmony_notes)

        all_freqs=melody_freqs+harmony_freqs

        wav_bytes=generate_wave_bytes_from_notes_frequencies(all_freqs)
    st.audio(BytesIO(wav_bytes), format='audio/wav')

    st.success("Music generated successfuly...")

    with st.expander("Composition summary"):
        st.text(composition)