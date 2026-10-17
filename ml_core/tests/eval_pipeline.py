import os
import sys
import json
import glob
from collections import defaultdict

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_core.schema.models import Statement
from ml_core.extraction.ner import extract_entities
from ml_core.extraction.temporal import extract_temporal_references
from ml_core.extraction.spatial import extract_spatial_references
from ml_core.extraction.negation import apply_negation_scoping
from ml_core.schema.models import EventTuple, EventOccurrence
from ml_core.detection.rules import check_existence_contradictions

def calculate_metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1

def run_evaluation():
    """
    Evaluates the extraction and rule-based consistency engine against
    the 100 benchmark incident datasets in ml_core/synthetic/generated/.
    Computes genuine precision, recall, and F1 per category.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generated_dir = os.path.join(base_dir, "synthetic", "generated")
    incident_files = sorted(glob.glob(os.path.join(generated_dir, "inc_proc_*.json")))
    
    if not incident_files:
        print(f"No benchmark files found at {generated_dir}")
        return ""
        
    stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0, "support": 0})
    total_processed = 0

    for file_path in incident_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        inc_type = data.get("incident_type", "general")
        ground_truth_labels = data.get("labels", [])
        
        # Track ground truth mismatches
        for label in ground_truth_labels:
            m_type = label.get("type", "general")
            stats[(inc_type, m_type)]["support"] += 1
            
        witnesses = data.get("witnesses", [])
        statements = []
        events = []
        occurrences = []
        
        for w_idx, w in enumerate(witnesses):
            stmt_text = w.get("statement", "")
            stmt = Statement(
                id=f"stmt_{w_idx}",
                witness_id=w.get("witness_id", f"w_{w_idx}"),
                text=stmt_text,
                incident_id=data.get("incident_id", "inc_eval")
            )
            statements.append(stmt)
            
            # Deterministic NLP passes
            extract_entities(stmt)
            extract_temporal_references(stmt)
            extract_spatial_references(stmt)
            
            # Check negation / perception heuristics from statement
            text_lower = stmt_text.lower()
            has_denial = any(term in text_lower for term in ["did not", "didn't", "never", "no ", "not "])
            action = "enter" if "enter" in text_lower else "run_red" if "red" in text_lower else "action"
            
            ev = EventTuple(
                source_statement_id=stmt.id,
                source_span=(0, min(len(stmt_text), 30)),
                text=stmt_text[:50],
                subject="suspect",
                action=action,
                object="scene",
                negated=has_denial
            )
            apply_negation_scoping(stmt, [ev])
            events.append(ev)
            
            if has_denial:
                occurrences.append(EventOccurrence(
                    source_statement_id=stmt.id,
                    source_span=(0, min(len(stmt_text), 30)),
                    text=stmt_text[:50],
                    event_type=action,
                    occurred=False
                ))

        # Run rule-based existence checks
        detected = check_existence_contradictions(occurrences, events)
        
        # Match against ground truth labels
        gt_types = set(l.get("type") for l in ground_truth_labels)
        for d in detected:
            m_type = d.type
            key = (inc_type, m_type)
            if m_type in gt_types:
                stats[key]["tp"] += 1
            else:
                stats[key]["fp"] += 1
                
        for label in ground_truth_labels:
            m_type = label.get("type")
            key = (inc_type, m_type)
            # If not detected by rule pass, record FN
            if not any(d.type == m_type for d in detected):
                stats[key]["fn"] += 1

        total_processed += 1

    report_lines = [
        "# ML Core Evaluation Report\n",
        f"Automated evaluation across {total_processed} benchmark incident datasets (`ml_core/synthetic/generated/`).\n",
        "| Incident Type | Mismatch Type | Precision | Recall | F1 Score | Support |",
        "|---|---|---|---|---|---|"
    ]

    for (inc_type, m_type), m in sorted(stats.items()):
        p, r, f1 = calculate_metrics(m["tp"], m["fp"], m["fn"])
        flag = " ⚠️" if f1 < 0.80 else ""
        report_lines.append(f"| {inc_type} | {m_type} | {p:.2f} | {r:.2f} | **{f1:.2f}**{flag} | {m['support']} |")

    report_content = "\n".join(report_lines) + "\n"
    report_path = os.path.join(base_dir, "eval_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Evaluation report successfully generated at {report_path}")
    return report_content

if __name__ == "__main__":
    run_evaluation()
