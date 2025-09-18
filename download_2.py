import os
import json
import requests
import pandas as pd
from urllib.parse import urlparse

Urls = ['https://query.gtios.com/data/TARGETconnect/queries', 'https://query.gtios.com/data/TARGETconnectV2/appointment_bookings', 'https://query.gtios.com/data/TARGETconnectV2/appointment_slots', 'https://query.gtios.com/data/TARGETconnectV2/students' ]
username = os.getenv("USERNAME")
ps_var =  os.getenv("PASSWORD")
password = ps_var.strip('_')

def download_and_convert(urls, username, password, output_dir='data/'):
    """
    Downloads JSON data from each URL, saves it to a .json file,
    and converts it to a .csv file using the same name.
    """
    os.makedirs(output_dir, exist_ok=True)
    for url in urls:
        try:
            # Extract filename from the URL endpoint
            endpoint = url.rstrip('/').split('/')[-1]
            json_filename = os.path.join(output_dir, f"{endpoint}.json")
            csv_filename = os.path.join(output_dir, f"{endpoint}.csv")

            # Download JSON data
            response = requests.get(url, auth=(username, password))
            response.raise_for_status()
            json_data = response.json()

            # Save JSON to file
            with open(json_filename, 'w') as f:
                json.dump(json_data, f, indent=4)
            print(f"Saved JSON to {json_filename}")

            # Convert to CSV (assumes data is under a 'data' key)
            if 'data' in json_data and isinstance(json_data['data'], list):
                df = pd.DataFrame(json_data['data'])
                df.to_csv(csv_filename, index=False)
                print(f"Converted to CSV: {csv_filename}")
            else:
                print(f"No 'data' key with a list found in JSON from {url}. Skipping CSV conversion.")

        except Exception as e:
            print(f"Failed to process {url}: {e}")
    
    # === COMMIT & PUSH ===
    commit_message = f"Update data - {datetime.utcnow().isoformat()}"
    
    subprocess.run(["git", "config", "--global", "user.email", "falaknaazkhxn@gmail.com"])
    subprocess.run(["git", "config", "--global", "user.name", "falaknaazkhan14"])
    
    subprocess.run(["git", "add"])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

download_and_convert(urls, username, password)
