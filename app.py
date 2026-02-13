import streamlit as st
import os
import zipfile
import subprocess
import sys

st.set_page_config(page_title="Mashup Web Service", page_icon="🎵")

st.title("🎵 Mashup Web Service")
st.write("Enter details to create and receive your custom audio mashup.")

# Input fields 
singer = st.text_input("Singer Name", value="Sharry Maan")
n_videos = st.number_input("# of videos", min_value=1, value=20)
duration = st.number_input("duration of each video (sec)", min_value=1, value=30)
email_id = st.text_input("Email Id")

if st.button("Submit"): # [cite: 37]
    if not singer or not email_id or "@" not in email_id:
        st.error("Please provide valid inputs and a correct email.") [cite: 40]
    elif n_videos <= 10 or duration <= 20:
        st.error("Constraints: Videos must be > 10 and Duration must be > 20.")
    else:
        with st.spinner("Processing..."):
            output_mp3 = "result.mp3"
            output_zip = "result.zip"
            
            # Use absolute path for the script for reliability
            script_path = os.path.join(os.getcwd(), "102303993.py")

            # Run the script
            process = subprocess.run([
                sys.executable, script_path, 
                singer, str(n_videos), str(duration), output_mp3
            ], capture_output=True, text=True)

            if os.path.exists(output_mp3):
                # Create Zip 
                with zipfile.ZipFile(output_zip, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success(f"Success! Mashup created for {singer}.")
                
                with open(output_zip, "rb") as f:
                    st.download_button("Download Zip File", f, file_name=output_zip)
            else:
                st.error("Execution failed. Check your logs.")
                with st.expander("Technical Error Log"):
                    st.code(process.stderr)