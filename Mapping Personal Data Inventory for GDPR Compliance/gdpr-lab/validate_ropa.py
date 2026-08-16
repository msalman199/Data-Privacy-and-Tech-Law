import csv

def validate_ropa(file_path: str) -> list:
    """
    Check the RoPA CSV file for missing lawful_basis or retention_period.

    Args:
        file_path: Path to the data_inventory.csv file

    Returns:
        List of process_ids that have missing required fields
    """
    missing_rows = []

    # TODO 1: Open the CSV file using open() and csv.DictReader
    # TODO 2: Loop through each row
    # TODO 3: If lawful_basis or retention_period is empty, add process_id to missing_rows
    # TODO 4: Return missing_rows

    pass


if __name__ == "__main__":
    result = validate_ropa("data_inventory.csv")
    if result:
        print("Rows missing required fields:", result)
    else:
        print("All rows have lawful basis and retention period defined.")
