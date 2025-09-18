import requests
import os
from datetime import datetime
import subprocess
import re
import json

# === CONFIGURATION ===
URL = "https://query.gtios.com/data/TARGETconnect/queries"  # Replace with your actual data source
FILENAME = "data/downloaded_data.csv"  # Save inside 'data' folder
json_file = "data/downloaded_data.json"  # Save inside 'data' folder
temp_file = "data/sample_output.txt"  # Save inside 'data' folder
username = os.getenv("USERNAME")
ps_var =  os.getenv("PASSWORD")
password = ps_var.strip('_')



# Use HTTP Basic Authentication
response = requests.get(URL, auth=(username, password))
response.raise_for_status()


# Parse JSON from the response
json_data = response.json()

# Ensure the directory exists
os.makedirs(os.path.dirname(json_file), exist_ok=True)

# Save JSON to file
with open(json_file, 'w') as f:
    json.dump(json_data, f, indent=4)

print(f"JSON saved to {json_file}")

os.makedirs(os.path.dirname(FILENAME), exist_ok=True)

# Convert "data" list to a DataFrame
df = pd.DataFrame(json_data['data'])

# Save DataFrame to CSV
df.to_csv(FILENAME, index=False)

print(f"CSV saved to {csv_file_path}")

# print(f"Downloaded file saved to {FILENAME}")

# === COMMIT & PUSH ===
commit_message = f"Update data - {datetime.utcnow().isoformat()}"

subprocess.run(["git", "config", "--global", "user.email", "falaknaazkhxn@gmail.com"])
subprocess.run(["git", "config", "--global", "user.name", "falaknaazkhan14"])

subprocess.run(["git", "add", FILENAME])
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push"])












# TOKEN = os.getenv("DATA_API_TOKEN")  # Loaded from GitHub secret
# HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# # === DOWNLOAD ===
# response = requests.get(URL, headers=HEADERS)
# response.raise_for_status()



# print(username)
# os.makedirs(os.path.dirname(temp_file), exist_ok=True)
# with open(FILENAME, "w") as f:
#     f.write(username)
