import streamlit as st
import os
import zipfile
import subprocess
import sys

# Set up page configuration
st.set_page_config(page_title="Mashup Web Service", page_icon="🎵")

st.title("🎵 Mashup Web Service")
st.write("Enter details to create and receive your custom audio mashup.")

# Input fields as per Assignment requirements [cite: 29, 38]
singer = st.text_input("Singer Name", value="Sharry Maan")
n_videos = st.number_input("# of videos", min_value=1, value=20)
duration = st.number_input("duration of each video (sec)", min_value=1, value=30)
email_id = st.text_input("Email Id")

if st.button("Submit"):
    # Basic Validation [cite: 25, 40]
    if not singer or not email_id or "@" not in email_id:
        st.error("Email id must be correct")
    elif n_videos <= 10 or duration <= 20:
        st.error("Constraints: Videos must be > 10 and Duration must be > 20.")
    else:
        with st.spinner("Processing..."):
            output_mp3 = "result.mp3"
            output_zip = "result.zip"
            
            # Clean up old files from previous runs
            for f in [output_mp3, output_zip]:
                if os.path.exists(f): 
                    os.remove(f)

            # Execution paths
            python_path = sys.executable
            script_path = os.path.join(os.getcwd(), "102303993.py")

            # Run Program 1 via subprocess [cite: 12]
            process = subprocess.run([
                python_path, script_path, 
                singer, str(n_videos), str(duration), output_mp3
            ], capture_output=True, text=True)

            # Check if the file was created successfully
            if os.path.exists(output_mp3):
                # Create result in zip format 
                with zipfile.ZipFile(output_zip, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success(f"Success! Mashup created for {singer}.")
                
                # Provide download button for the zip file
                with open(output_zip, "rb") as f:
                    st.download_button("Download Zip File", f, file_name=output_zip)
                
                st.info(f"The result is ready for {email_id}.")
            else:
                st.error("The mashup could not be generated due to YouTube restrictions on the cloud.")
                with st.expander("Show Technical Logs"):
                    st.code(process.stderr)