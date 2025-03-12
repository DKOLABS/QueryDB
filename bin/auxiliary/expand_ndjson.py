import json
from pathlib import Path
from helper import make_safe_filename

ROOT_DIR = Path(__file__).parent.parent.parent


def expand_ndjson(ndjson_file, output_dir):

    with open(ndjson_file, "r", encoding="utf-8") as infile:
        for index, line in enumerate(infile):
            try:
                json_object = json.loads(line)["result"]
            except json.JSONDecodeError as e:
                print(f"Skipping line {index} due to decoding error: {e}")
                continue

            # Use index or a unique field to name the file
            output_file = output_dir / f"{json_object['title']}.json"

            # Save the individual JSON object to a file
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(json_object, outfile, indent=4)

            print(f"Saved JSON object to {output_file}")


if __name__ == "__main__":
    # Example usage
    ndjson_file = ROOT_DIR / "data" / "raw" / "all_searches.json"
    output_dir = ROOT_DIR / "data" / "parsed"
    expand_ndjson(ndjson_file, output_dir)
