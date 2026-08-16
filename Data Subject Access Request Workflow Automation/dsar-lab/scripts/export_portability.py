import sqlite3
import json
import hashlib

def fetch_customer_data(email: str) -> dict:
    """
    Query customer.db for all records matching the given email.

    Returns:
        Dictionary of customer fields
    """
    # TODO: connect to tickets/customer.db
    # TODO: query row matching email
    # TODO: convert row to dict and return
    pass

def build_json_bundle(data: dict, output_path: str) -> str:
    """
    Write data to a JSON file and return a SHA-256 checksum of the file.

    Args:
        data: Customer data dictionary
        output_path: File path to write JSON bundle

    Returns:
        Hex checksum string
    """
    # TODO: write data as formatted JSON to output_path
    # TODO: compute sha256 hash of the file contents
    # TODO: return hex digest
    pass

if __name__ == "__main__":
    data = fetch_customer_data("ahmed@example.com")
    checksum = build_json_bundle(data, "reports/portability_bundle.json")
    print(f"Bundle created. Checksum: {checksum}")
