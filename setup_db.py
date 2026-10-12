"""
setup_db.py
===========
Repeatable database initialisation script for the
Employee Benefits Enrollment QA Validation Project.

What this script does
---------------------
1. Reads schema.sql and creates all tables in a SQLite file
   (default: benefits_enrollment.db).
2. Loads the valid baseline CSV files from data/ into the
   corresponding tables.
3. Enables foreign-key enforcement for every connection it opens
   (SQLite requires this pragma per connection).

Usage
-----
  # Create / reset the default database
  python setup_db.py

  # Use a custom database path
  python setup_db.py --db my_custom.db

  # Reset using a specific schema file
  python setup_db.py --schema schema.sql --db benefits_enrollment.db

IMPORTANT: Re-running this script drops and recreates all tables,
so it is safe to run as many times as needed during development.
Do NOT point it at a database that contains data you want to keep.
"""

import argparse
import csv
import sqlite3
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to this script's location)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DEFAULT_DB = BASE_DIR / "benefits_enrollment.db"
DEFAULT_SCHEMA = BASE_DIR / "schema.sql"
DATA_DIR = BASE_DIR / "data"

# Map CSV filename -> table name for baseline (valid) data only.
# Order matters: parent tables must be loaded before child tables.
BASELINE_FILES = [
    ("employees.csv",     "employees"),
    ("benefit_plans.csv", "benefit_plans"),
    ("dependents.csv",    "dependents"),
    ("enrollments.csv",   "enrollments"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_connection(db_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection with foreign-key enforcement enabled."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def apply_schema(conn: sqlite3.Connection, schema_path: Path) -> None:
    """Execute the SQL schema file (drops and recreates all tables)."""
    sql = schema_path.read_text(encoding="utf-8")
    conn.executescript(sql)
    print(f"  [OK] Schema applied from {schema_path.name}")


def load_csv_to_table(conn: sqlite3.Connection, csv_path: Path, table: str) -> int:
    """
    Read a CSV file and INSERT all rows into *table*.

    The CSV header row must exactly match the column names in the table.
    Returns the number of rows inserted.

    Why we use executemany with parameterised queries
    -------------------------------------------------
    Parameterised queries prevent SQL-injection and handle edge cases
    (NULL values, text with commas or quotes) automatically.
    """
    if not csv_path.exists():
        print(f"  [SKIP] {csv_path.name} not found — table '{table}' left empty.")
        return 0

    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    if not rows:
        print(f"  [SKIP] {csv_path.name} is empty — table '{table}' left empty.")
        return 0

    columns = rows[0].keys()
    placeholders = ", ".join("?" for _ in columns)
    col_list = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

    # Convert empty strings to None so SQLite stores them as NULL.
    def normalise(row: dict) -> tuple:
        return tuple(None if v == "" else v for v in row.values())

    conn.executemany(sql, [normalise(r) for r in rows])
    conn.commit()
    print(f"  [OK] Loaded {len(rows):>3} row(s) from {csv_path.name} -> {table}")
    return len(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def initialise_database(db_path: Path, schema_path: Path) -> None:
    """Drop, recreate, and populate the database from baseline CSV files."""
    print(f"\nInitialising database: {db_path}")
    print(f"Schema file          : {schema_path}\n")

    conn = get_connection(db_path)

    print("Applying schema …")
    apply_schema(conn, schema_path)

    print("\nLoading baseline data …")
    total = 0
    for filename, table in BASELINE_FILES:
        csv_path = DATA_DIR / filename
        total += load_csv_to_table(conn, csv_path, table)

    conn.close()
    print(f"\nDone. {total} total row(s) loaded into {db_path.name}.")


def print_summary(db_path: Path) -> None:
    """Print row counts for every table as a quick sanity check."""
    conn = get_connection(db_path)
    tables = ["employees", "benefit_plans", "dependents", "enrollments"]
    print("\nRow counts after initialisation:")
    print(f"  {'Table':<20} {'Rows':>5}")
    print("  " + "-" * 27)
    for t in tables:
        try:
            (count,) = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()
        except sqlite3.OperationalError:
            count = "ERROR"
        print(f"  {t:<20} {count:>5}")
    conn.close()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialise the Employee Benefits Enrollment database."
    )
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB),
        help=f"Path to the SQLite database file (default: {DEFAULT_DB.name})",
    )
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA),
        help=f"Path to the SQL schema file (default: {DEFAULT_SCHEMA.name})",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    schema_path = Path(args.schema)

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    initialise_database(db_path, schema_path)
    print_summary(db_path)
