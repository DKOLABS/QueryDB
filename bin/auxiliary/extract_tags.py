import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

input_file = ROOT_DIR / "scratch" / "note.txt"

# Read the file
with open(input_file, "r") as file:
    content = file.read()

# Define regex patterns
datamodel_pattern = r"datamodel\s*=\s*(\w+)"
index_pattern = r'index\s*=\s*"?(\w+)"?|index\s*IN\s*\(([^)]+)\)'

# Extract datamodels
datamodels = re.findall(datamodel_pattern, content)

# Extract indexes
indexes = []
index_matches = re.findall(index_pattern, content)
for match in index_matches:
    if match[0]:  # Single index
        indexes.append(match[0])
    if match[1]:  # Multiple indexes
        indexes.extend(match[1].replace('"', "").split(","))

# Clean up indexes list
indexes = [index.strip() for index in indexes]

print("Datamodels:", datamodels)
print("Indexes:", indexes)
