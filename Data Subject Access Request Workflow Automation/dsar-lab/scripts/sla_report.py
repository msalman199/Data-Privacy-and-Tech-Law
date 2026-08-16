import sqlite3
from datetime import datetime

def get_overdue_requests(db_path: str = "tickets/dsar.db") -> list:
    """
    Return all requests where sla_deadline has passed and status != 'completed'.
    """
    # TODO: query requests table for overdue, non-completed rows
    pass

def generate_report(db_path: str = "tickets/dsar.db", output_path: str = "reports/compliance_report.txt") -> None:
    """
    Write a summary report: total requests, completed, overdue, and
    percentage compliance (completed within SLA / total).
    """
    # TODO: query totals from the requests table
    # TODO: calculate compliance percentage
    # TODO: write formatted summary to output_path
    pass

if __name__ == "__main__":
    generate_report()
    print("Report generated at reports/compliance_report.txt")
