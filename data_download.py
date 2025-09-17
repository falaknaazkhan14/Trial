import requests
import os
from datetime import datetime
import subprocess

# === CONFIGURATION ===
URL = "https://example.com/data.csv"  # Replace with your actual data source
FILENAME = "data/downloaded_data.csv"  # Save inside 'data' folder
TOKEN = os.getenv("DATA_API_TOKEN")  # Loaded from GitHub secret
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# === DOWNLOAD ===
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
with open(FILENAME, "wb") as f:
    f.write(response.content)

print(f"Downloaded file saved to {FILENAME}")

# === COMMIT & PUSH ===
commit_message = f"Update data - {datetime.utcnow().isoformat()}"

subprocess.run(["git", "config", "--global", "user.email", "bot@example.com"])
subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions Bot"])

subprocess.run(["git", "add", FILENAME])
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push"])
