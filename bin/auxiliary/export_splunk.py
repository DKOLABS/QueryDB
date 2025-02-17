import requests
import json
from pathlib import Path
from helper import make_safe_filename

# Configuration
SPLUNK_HOST = "ENDPOINT"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_FOLDER = Path(ROOT_DIR / "json_data")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Perform the Splunk search
search_url = f"{SPLUNK_HOST}/services/saved/searches?output_mode=json"
headers = {
    "Content-Type": "application/json",
}

# Start the search job
response = requests.get(search_url, auth=(USERNAME, PASSWORD), headers=headers, verify=False)

if response.status_code == 200:
    results = json.loads(response.text)
    for search in results['entry']:
        file_name = f'{make_safe_filename(search['name'])}.json'
        output_file = Path(OUTPUT_FOLDER / file_name)
        with open(output_file, 'w') as f:
            json.dump(search, f, indent=4)

else:
    print(f"Failed to start search job: {response.status_code}")
    print(response.text)
