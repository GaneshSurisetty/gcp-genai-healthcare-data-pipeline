
import csv
from pathlib import Path


def validate_healthcare_data(file_path):
    valid_records = []
    invalid_records = []
    seen_encounters = set()

    with open(file_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            errors = []
            encounter_id = row["encounter_id"]
            patient_id = row["patient_id"]

            if not encounter_id or not patient_id:
                errors.append("Missing required identifier")

            if encounter_id in seen_encounters:
                errors.append("Duplicate encounter ID")

            try:
                amount = float(row["claim_amount"])
                if amount < 0:
                    errors.append("Negative claim amount")
            except (ValueError, TypeError):
                errors.append("Invalid claim amount")

            if encounter_id:
                seen_encounters.add(encounter_id)

            if errors:
                invalid_records.append({
                    "record": row,
                    "errors": errors
                })
            else:
                valid_records.append(row)

    return valid_records, invalid_records


if __name__ == "__main__":
    input_file = Path("data/patient_encounters.csv")
    valid, invalid = validate_healthcare_data(input_file)

    print("Healthcare Data Quality Report")
    print("------------------------------")
    print(f"Total Records: {len(valid) + len(invalid)}")
    print(f"Valid Records: {len(valid)}")
    print(f"Invalid Records: {len(invalid)}")

    for item in invalid:
        print(
            f"Rejected {item['record']['encounter_id']}: "
            f"{', '.join(item['errors'])}"
        )
