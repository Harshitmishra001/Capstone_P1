import json
import time
from pathlib import Path
from ml_core.orchestrator import analyze_incident

OUTPUT_FILE = Path("theft_case_output.json")

def test_theft_case():
    print("=" * 75)
    print(" SILENT WITNESS — MULTI-WITNESS THEFT CASE DEMO (5 WITNESSES)")
    print("=" * 75)

    # 5 distinct eyewitness testimonies (8 sentences total) for the jewelry store heist
    witness_statements = [
        # Witness 1: Store Security Guard (Inside)
        "At 8:15 PM, two masked men armed with handguns entered the Tanishq jewelry store on MG Road. "
        "They smashed the glass display counters and stole diamond necklaces.",

        # Witness 2: Tea Stall Vendor (Across the street)
        "Around 8:20 PM, I saw three men running out of the jewelry store carrying black duffel bags. "
        "The robbers were not holding handguns; they were armed with heavy iron crowbars.",

        # Witness 3: Auto Rickshaw Driver (At the junction)
        "The primary robber was wearing a dark leather jacket and fled on a black motorcycle towards the station.",

        # Witness 4: Pedestrian Shopper (On the sidewalk)
        "The main suspect was wearing a bright red hoodie with beige cargo pants. "
        "They did not escape on a motorcycle; they jumped into a silver getaway sedan and sped towards the highway.",

        # Witness 5: Store Cashier (Emergency responder view)
        "The store alarm went off at 8:30 PM after the thieves fled with fifty lakhs in jewelry."
    ]

    print("\n--- INPUT WITNESS TESTIMONIES (5 VANTAGE POINTS) ---")
    roles = [
        "Witness 1 (Store Security)",
        "Witness 2 (Tea Vendor Across Street)",
        "Witness 3 (Auto Rickshaw Driver)",
        "Witness 4 (Pedestrian Shopper)",
        "Witness 5 (Store Cashier)"
    ]
    for role, text in zip(roles, witness_statements):
        print(f"\n[{role}]:\n\"{text}\"")

    print("\n" + "-" * 75)
    print("Executing full NLP pipeline via local SmolLM-3B (http://172.19.121.89:1234)...")
    start_time = time.time()

    # Run central orchestrator
    result = analyze_incident(witness_statements)
    elapsed = time.time() - start_time

    # Save output to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Pipeline completed in {elapsed:.2f} seconds!")
    print(f"Structured JSON output saved to: {OUTPUT_FILE.resolve()}")
    print("-" * 75)

    # Display Metrics & Summary
    print("\n--- EXTRACTION & CONTRADICTION SUMMARY ---")
    print(f"Total Witnesses/Statements : {result['metrics']['total_statements']}")
    print(f"Entities Recognized (NER)  : {result['metrics']['total_entities']}")
    print(f"Events Extracted (S-V-O)   : {result['metrics']['total_events']}")
    print(f"Claims Generated           : {result['metrics']['total_claims']}")
    print(f"Contradictions Flagged     : {result['metrics']['total_contradictions']}")

    # Display clean JSON preview on terminal
    print("\n" + "=" * 75)
    print(" TERMINAL DISPLAY: STRUCTURED JSON OUTPUT")
    print("=" * 75)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_theft_case()
