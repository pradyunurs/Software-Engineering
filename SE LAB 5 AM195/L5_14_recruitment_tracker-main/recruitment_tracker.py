
"""Recruitment tracker with SQLite storage and static-analysis fixes."""

import ast
import csv
import operator
import sqlite3
from pathlib import Path


conn = sqlite3.connect(":memory:")

conn.execute(
    """
    CREATE TABLE applicants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        expected_salary INTEGER,
        status TEXT
    )
    """
)


def evaluate_salary_rule(salary_rule):
    """Evaluate a salary expression containing numbers and basic arithmetic."""
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.floordiv,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = operators.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported arithmetic operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero is not allowed.")

            return operation(left, right)

        raise ValueError("Invalid salary rule.")

    try:
        expression = ast.parse(salary_rule, mode="eval")
        result = evaluate(expression)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError("Invalid salary rule.") from error

    if result < 0:
        raise ValueError("Salary limit cannot be negative.")

    return result


def add_applicant(name, role, expected_salary, status="applied"):
    """Add an applicant to the database."""
    conn.execute(
        """
        INSERT INTO applicants (name, role, expected_salary, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, salary_rule):
    """Return applicant names matching a role and salary limit."""
    rows = conn.execute(
        """
        SELECT name, expected_salary
        FROM applicants
        WHERE role = ?
        """,
        (role,),
    ).fetchall()

    limit = evaluate_salary_rule(salary_rule)

    return [
        name
        for name, salary in rows
        if salary <= limit
    ]


def update_status(applicant_id, status):
    """Update an applicant's status."""
    try:
        conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise


def export_report(path):
    """Export applicant information to a CSV file."""
    rows = conn.execute(
        "SELECT name, role, status FROM applicants"
    ).fetchall()

    with Path(path).open(
        "w",
        newline="",
        encoding="utf-8",
    ) as report_file:
        writer = csv.writer(report_file)
        writer.writerows(rows)


def count_by_status(status):
    """Return the number of applicants with a given status."""
    result = conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?",
        (status,),
    ).fetchone()

    return result[0]


def main():
    """Run a demonstration of the recruitment tracker."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)

    update_status(1, "interview")

    print(shortlist("analyst", "500000 + 150000"))

    export_report("applicants_report.csv")

    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
