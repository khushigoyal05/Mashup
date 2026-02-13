import streamlit as st
import os
import zipfile
import smtplib
from email.message import EmailMessage
import subprocess

st.set_page_config(page_title="Mashup Web Service", page_icon="🎵")

st.title("🎵 Mashup Web Service")
st.markdown("Enter details to create and receive your custom audio mashup.")

# Input fields as per Program 2 requirements
singer = st.text_input("Singer Name", placeholder="e.g. Sharry Maan")
n_videos = st.number_input("# of videos (Must be > 10)", min_value=1, value=20)
duration = st.number_input("Duration of each video (sec) (Must be > 20)", min_value=1, value=30)
email_id = st.text_input("Email Id", placeholder="yourname@gmail.com")

if st.button("Submit"):
    # Basic Validation
    if not singer or not email_id:
        st.error("Please fill in all fields.")
    elif n_videos <= 10 or duration <= 20:
        st.error("Constraints: Videos > 10 and Duration > 20.")
    elif "@" not in email_id:
        st.error("Please provide a valid email address.")
    else:
        with st.spinner("Processing your mashup... this involves downloading and merging audio."):
            output_mp3 = "result.mp3"
            output_zip = "result.zip"
            
            # Using subprocess to run your Program 1 script (102303993.py)
            try:
                # Command format: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
                subprocess.run([
                    "python", "102303993.py", 
                    singer, str(n_videos), str(duration), output_mp3
                ], check=True)
                
                # Create the Zip file as required
                with zipfile.ZipFile(output_zip, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success(f"Success! Mashup created for {singer}.")
                
                # Manual download button (since Email SMTP requires private credentials)
                with open(output_zip, "rb") as f:
                    st.download_button("Download Zip File", f, file_name=output_zip)
                
                st.info("Assignment Note: To send the email automatically, an SMTP server must be configured.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")