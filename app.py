import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
import os

# App ရဲ့ ခေါင်းစဉ်
st.set_page_config(page_title="MLBB Auto Editor", page_icon="🎮")
st.title("🇲🇲 MLBB Auto-Edit Web App")
st.write("သင့်ရဲ့ Gameplay ဗီဒီယိုနဲ့ မြန်မာသီချင်းကို ရွေးပေးလိုက်ပါ")

# ဖိုင်တင်ရန် နေရာများ
uploaded_video = st.file_uploader("MLBB Gameplay Video (MP4) တင်ပါ", type=["mp4", "mov"])
uploaded_audio = st.file_uploader("မြန်မာသီချင်း (MP3) တင်ပါ", type=["mp3", "wav"])

if uploaded_video and uploaded_audio:
    if st.button("Edit စလုပ်မယ် ✨"):
        with st.spinner('AI က ဗီဒီယိုကို မြန်မာသီချင်းနဲ့ ညှိပြီး တည်းဖြတ်ပေးနေပါတယ်...'):
            try:
                # ဖိုင်များကို ခေတ္တသိမ်းဆည်းခြင်း
                with open("temp_v.mp4", "wb") as f:
                    f.write(uploaded_video.getbuffer())
                with open("temp_a.mp3", "wb") as f:
                    f.write(uploaded_audio.getbuffer())

                # Video နှင့် Audio ကို Load လုပ်ခြင်း
                video = VideoFileClip("temp_v.mp4")
                audio = AudioFileClip("temp_a.mp3")
                
                # ဗီဒီယိုကို သီချင်းအရှည်အတိုင်း (သို့) သီချင်းကို ဗီဒီယိုအရှည်အတိုင်း ညှိခြင်း
                duration = min(video.duration, audio.duration)
                final_video = video.subclip(0, duration).set_audio(audio.set_duration(duration))
                
                # Result ထုတ်ခြင်း
                output_path = "mlbb_final_edit.mp4"
                final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

                # Video ပြသခြင်းနှင့် Download ပေးခြင်း
                st.success("တည်းဖြတ်ပြီးပါပြီ!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="ဗီဒီယိုကို ဒေါင်းလုဒ်ဆွဲမည် ⬇️",
                        data=file,
                        file_name="MLBB_AutoEdit_Myanmar.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"အမှားတစ်ခုရှိနေပါတယ်: {e}")
                
