import sqlite3
from datetime import datetime, timedelta

DB_PATH = "tickets/dsar.db"
SLA_DAYS = 30  # GDPR standard; adjust for PDPL if needed

def create_request(email: str, request_type: str) -> int:
    """
    Insert a new DSAR ticket into the database.

    Args:
        email: Data subject's email address
        request_type: One of 'access', 'deletion', 'portability', 'rectification'

    Returns:
        The new request ID
    """
    # TODO: validate request_type against allowed values
    # TODO: calculate sla_deadline = now + SLA_DAYS
    # TODO: insert row into requests table
    # TODO: return the new row's id
    pass

if __name__ == "__main__":
    # TODO: call create_request() with sample data and print the ID
    pass
