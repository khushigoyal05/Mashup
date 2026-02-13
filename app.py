import streamlit as st
import os
import zipfile
import subprocess
import sys

st.set_page_config(page_title="Mashup Web Service", page_icon="🎵")

st.title("🎵 Mashup Web Service")
st.write("Enter details to create and receive your custom audio mashup.")

# Inputs [cite: 30, 32, 34, 35]
singer = st.text_input("Singer Name", value="Sharry Maan")
n_videos = st.number_input("# of videos (Must be > 10)", min_value=1, value=20)
duration = st.number_input("Duration of each video (sec) (Must be > 20)", min_value=1, value=30)
email_id = st.text_input("Email Id")

if st.button("Submit"):
    if not singer or not email_id or "@" not in email_id:
        st.error("Please provide valid inputs and a correct email.")
    elif n_videos <= 10 or duration <= 20:
        st.error("Constraint Violation: Videos must be > 10 and Duration > 20.")
    else:
        with st.spinner("Creating Mashup..."):
            output_mp3 = "result.mp3"
            output_zip = "result.zip"
            
            # Using sys.executable to ensure the correct python path on Cloud
            python_path = sys.executable
            script_path = os.path.join(os.getcwd(), "102303993.py")

            # Run Program 1 [cite: 12]
            process = subprocess.run([
                python_path, script_path, 
                singer, str(n_videos), str(duration), output_mp3
            ], capture_output=True, text=True)

            if process.returncode != 0:
                st.error(f"Execution Error: {process.stderr}")
            else:
                # Zip the result [cite: 39]
                with zipfile.ZipFile(output_zip, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success(f"Mashup for {singer} is ready!")
                
                with open(output_zip, "rb") as f:
                    st.download_button("Download Zip File", f, file_name=output_zip)
                
                st.info(f"The result is ready for {email_id}. (SMTP configuration needed for auto-email)")