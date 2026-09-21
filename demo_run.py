import json
import requests
import re
from pathlib import Path

API_URL = "http://127.0.0.1:8000/analyze"
TRANSCRIPTS_DIR = Path("ml_core/synthetic/transcripts")

def extract_witness_statements(file_path: Path) -> list:
    """Parses a transcript file splitting by '### Witness X' headers."""
    if not file_path.exists():
        raise FileNotFoundError(f"Transcript not found: {file_path}")
        
    content = file_path.read_text(encoding="utf-8")
    
    # Split by '### Witness'
    parts = re.split(r'###\s+Witness\s+\d+', content)
    # The first split is usually empty or intro text
    statements = [p.strip() for p in parts if p.strip()]
    return statements

def main():
    print("--- Silent Witness Local Demo ---")
    
    # Pick one of the generated Indian-context transcripts
    target_file = TRANSCRIPTS_DIR / "marine_drive_hit_run.txt"
    print(f"Loading {target_file.name}...")
    
    statements = extract_witness_statements(target_file)
    
    # For a quick demo, we'll just send the first 4 witnesses so we don't wait too long
    # for the local 3B model to process all 20.
    demo_statements = statements[:4]
    
    print(f"Found {len(statements)} testimonies. Sending first {len(demo_statements)} to FastAPI backend...")
    
    payload = {"statements": demo_statements}
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("\n=== SUCCESS ===")
        print(f"Entities Found: {data['metrics']['total_entities']}")
        print(f"Events Extracted: {data['metrics']['total_events']}")
        print(f"Contradictions Detected: {data['metrics']['total_contradictions']}")
        print("\n--- JSON OUTPUT PREVIEW ---")
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the backend.")
        print("Did you start the FastAPI server? (Run: python server.py)")
        print("And is LM Studio running on port 1234?")
    except requests.exceptions.HTTPError as e:
        print(f"\nAPI Error: {e.response.text}")

if __name__ == "__main__":
    main()
