import csv
from datetime import datetime

def generate_ropa_report(input_file: str, output_file: str) -> None:
    """
    Read the data inventory CSV and generate a formatted RoPA report
    (plain text file) for the DPO.

    Args:
        input_file: Path to data_inventory.csv
        output_file: Path to save the report (e.g., ropa_report.txt)
    """
    # TODO 1: Open input_file and read rows with csv.DictReader
    # TODO 2: Open output_file for writing
    # TODO 3: Write a title line and generation date (use datetime.now())
    # TODO 4: For each row, write process_name, data_subject_category,
    #         sensitive_category, lawful_basis, and retention_period
    # TODO 5: Close both files (or use 'with' blocks)

    pass


if __name__ == "__main__":
    generate_ropa_report("data_inventory.csv", "ropa_report.txt")
    print("Report generated: ropa_report.txt")
