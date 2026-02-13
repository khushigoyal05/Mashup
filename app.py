import streamlit as st
import os
import zipfile
import subprocess
import sys

st.set_page_config(page_title="Mashup Web Service")
st.title("🎵 Mashup Web Service")

# Required UI Inputs 
singer = st.text_input("Singer Name", value="Sharry Mann")
n_videos = st.number_input("# of videos", min_value=1, value=20)
duration = st.number_input("duration of each video (sec)", min_value=1, value=30)
email_id = st.text_input("Email Id")

if st.button("Submit"):
    # Task: Check for correct Email id 
    if not singer or not email_id or "@" not in email_id:
        st.error("Email id must be correct")
    elif n_videos <= 10 or duration <= 20:
        st.error("Error: N must be > 10 and Y must be > 20")
    else:
        with st.spinner("Processing..."):
            output_mp3 = "result.mp3"
            output_zip = "result.zip"
            
            # Clean up old files
            if os.path.exists(output_mp3): os.remove(output_mp3)
            if os.path.exists(output_zip): os.remove(output_zip)

            # Run Program 1
            script_path = os.path.join(os.getcwd(), "102303993.py")
            process = subprocess.run([
                sys.executable, script_path, 
                singer, str(n_videos), str(duration), output_mp3
            ], capture_output=True, text=True)

            if os.path.exists(output_mp3):
                # Task: User should get the result in zip format 
                with zipfile.ZipFile(output_zip, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success("Mashup Complete!")
                with open(output_zip, "rb") as f:
                    st.download_button("Download Zip File", f, file_name=output_zip)
            else:
                st.error("The mashup could not be generated on the cloud due to YouTube (403) blocks.")
                with st.expander("View Logs"):
                    st.code(process.stderr)