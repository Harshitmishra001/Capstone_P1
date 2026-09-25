import json
import time
from pathlib import Path
from ml_core.orchestrator import analyze_incident

OUTPUT_FILE = Path("theft_case_output.json")

def test_theft_case():
    print("=" * 70)
    print(" SILENT WITNESS — DETAILED THEFT CASE DEMO")
    print("=" * 70)

    # 7-8 detailed sentences across two witnesses describing a jewelry store heist
    statement_1 = (
        "At 8:15 PM, two masked men armed with handguns entered the Tanishq jewelry store on MG Road. "
        "They shattered the glass display cases and stole diamond necklaces worth fifty lakhs. "
        "The primary suspect was wearing a heavy black leather jacket and dark blue jeans. "
        "They fled the scene on a black Yamaha motorcycle heading east towards the railway station."
    )

    statement_2 = (
        "Around 8:30 PM, I saw three men running out of the jewelry store on MG Road carrying black duffel bags. "
        "The suspects were not carrying handguns; they were holding large steel crowbars. "
        "The tall suspect was wearing a bright red hoodie with beige cargo pants. "
        "They did not escape on a motorcycle; they jumped into a silver getaway sedan and sped towards the highway."
    )

    statements = [statement_1, statement_2]

    print("\n--- INPUT WITNESS TESTIMONIES (8 DETAILED SENTENCES) ---")
    print(f"\n[Witness 1 - Store Security / Employee]:\n\"{statement_1}\"")
    print(f"\n[Witness 2 - Street Bystander]:\n\"{statement_2}\"")

    print("\n" + "-" * 70)
    print("Running NLP & Contradiction Detection pipeline via local SmolLM-3B...")
    start_time = time.time()

    # Run full orchestrator
    result = analyze_incident(statements)
    elapsed = time.time() - start_time

    # Save to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Pipeline completed in {elapsed:.2f} seconds!")
    print(f"Full JSON results saved to: {OUTPUT_FILE.resolve()}")
    print("-" * 70)

    # Display Metrics & Summary
    print("\n--- EXTRACTION & DETECTION SUMMARY ---")
    print(f"Total Statements Analyzed : {result['metrics']['total_statements']}")
    print(f"Entities Recognized (NER) : {result['metrics']['total_entities']}")
    print(f"Events Extracted (S-V-O)  : {result['metrics']['total_events']}")
    print(f"Claims Generated          : {result['metrics']['total_claims']}")
    print(f"Contradictions Flagged    : {result['metrics']['total_contradictions']}")

    # Display clean preview on terminal
    print("\n" + "=" * 70)
    print(" TERMINAL DISPLAY: STRUCTURED JSON OUTPUT")
    print("=" * 70)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_theft_case()
