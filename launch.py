import subprocess
import webbrowser
import time
import os

# Launch Streamlit app
subprocess.Popen(["streamlit", "run", "attendance_analysis.py"])

# Wait for server to start
time.sleep(3)

# Open in Chrome or default browser
url = "http://localhost:8501"
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
if os.path.exists(chrome_path):
    webbrowser.get(f'"{chrome_path}" %s').open(url)
else:
    webbrowser.open(url)
