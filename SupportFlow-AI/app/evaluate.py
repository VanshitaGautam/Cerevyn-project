"""Evaluate the classifier on the explicitly held-out test portion of sample_data/tickets.json."""
import json
from pathlib import Path
from app.classifier import classify_ticket

DATA_PATH = Path(__file__).resolve().parent.parent / "sample_data" / "tickets.json"


def main():
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    test_records = [record for record in records if record["split"] == "test"]
    if not test_records:
        raise SystemExit("No test records found.")

    category_correct = 0
    priority_correct = 0
    print(f"Evaluating {len(test_records)} held-out test tickets")
    for record in test_records:
        result = classify_ticket(record["message"])
        cat_ok = result["category"] == record["expected_category"]
        pri_ok = result["priority"] == record["expected_priority"]
        category_correct += int(cat_ok)
        priority_correct += int(pri_ok)
        print(
            f'{record["ticket_id"]}: category={result["category"]} '
            f'({"OK" if cat_ok else "MISMATCH"}), priority={result["priority"]} '
            f'({"OK" if pri_ok else "MISMATCH"})'
        )

    total = len(test_records)
    print(f"Category accuracy: {category_correct}/{total} = {category_correct / total:.1%}")
    print(f"Priority accuracy: {priority_correct}/{total} = {priority_correct / total:.1%}")


if __name__ == "__main__":
    main()
