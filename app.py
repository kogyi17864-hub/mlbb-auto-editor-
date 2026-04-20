import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import os

st.set_page_config(page_title="MLBB Pro Editor", page_icon="🎬")
st.title("🎬 MLBB Slow-Mo Editor")

video_file = st.file_uploader("MLBB Gameplay (MP4) တင်ပါ", type=['mp4'])
audio_file = st.file_uploader("သီချင်း (MP3) တင်ပါ", type=['mp3'])

if video_file and audio_file:
    if st.button("Slow Motion နဲ့ Edit မယ်"):
        with st.spinner("Slow Motion ထည့်ပြီး ဗီဒီယို ပြင်နေပါတယ်..."):
            # ယာယီသိမ်းခြင်း
            with open("temp_v.mp4", "wb") as f:
                f.write(video_file.read())
            with open("temp_a.mp3", "wb") as f:
                f.write(audio_file.read())

            video = VideoFileClip("temp_v.mp4")
            audio = AudioFileClip("temp_a.mp3")

            # ဗီဒီယို အရှည်ကို သီချင်းနဲ့ ညှိမယ်
            duration = min(video.duration, audio.duration)
            video = video.subclip(0, duration)

            # အလယ်ပိုင်းကို Slow Motion လုပ်ခြင်း (ဥပမာ- စက္ကန့် ၂၀ ကနေ ၃၀ ကြား)
            # ဗီဒီယိုရဲ့ ၅၀% ကနေ ၇၀% အပိုင်းကို 0.5x အနှေးလုပ်မယ်
            start_slow = duration * 0.4
            end_slow = duration * 0.7
            
            part1 = video.subclip(0, start_slow)
            part2 = video.subclip(start_slow, end_slow).fx(vfx.speedx, 0.5) # 0.5 က အနှေးနှုန်းပါ
            part3 = video.subclip(end_slow, duration)

            from moviepy.editor import concatenate_videoclips
            final_video = concatenate_videoclips([part1, part2, part3])
            
            # သီချင်းပြန်ထည့်မယ်
            final_video = final_video.set_audio(audio)
            
            # ဗီဒီယို ထုတ်မယ်
            output_path = "mlbb_slowmo.mp4"
            final_video.write_videofile(output_path, fps=24, codec="libx264")

            st.success("ပြုပြင်ပြီးပါပြီ!")
            with open(output_path, "rb") as file:
                st.download_button("Slow-Mo ဗီဒီယို သိမ်းမယ်", file, output_path)
                
