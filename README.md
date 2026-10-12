# Employee Benefits Enrollment — QA Validation

> **Simulated Learning Project** — All employees, plans, and enrollment data are
> entirely fictional. This project does not represent real healthcare, insurance,
> or benefits administration. It is designed as a portfolio project demonstrating
> foundational QA skills relevant to a Graduate Engineer Trainee role in Health
> and Welfare (HW) Technology.

---

## Table of Contents

1. [Objective](#objective)
2. [Scope and Limitations](#scope-and-limitations)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Business Rules](#business-rules)
6. [Setup Instructions](#setup-instructions)
7. [Running SQL Validations](#running-sql-validations)
8. [Running Tests](#running-tests)
9. [Test Data Overview](#test-data-overview)
10. [Key Commands Reference](#key-commands-reference)
11. [Uploading to GitHub](#uploading-to-github)

---

## Objective

Build and validate a simulated **Employee Benefits Enrollment** system to demonstrate:

- Test data preparation (valid and invalid CSV fixtures)
- Database schema design with SQLite constraints
- SQL-based data quality validation
- Automated pytest testing (positive and negative cases)
- QA documentation (test cases, defect log, execution report)

This project maps directly to skills listed in a Graduate Engineer Trainee – HW
Technology role: data validation, SQL checks, test execution, and defect reporting.

---

## Scope and Limitations

**In scope:**
- Fictional employees, benefit plans, dependents, and enrollments
- Business rule validation via SQL queries and pytest
- Constraint enforcement at the SQLite level where practical
- Repeatable test isolation using pytest `tmp_path` fixtures

**Out of scope / limitations:**
- Real personal, financial, or health information is not used
- No jurisdiction-specific insurance rules or regulatory compliance (HIPAA, ACA, etc.)
- No web UI or REST API
- Application-level enforcement of BR-04 and BR-08 is via SQL checks, not DB triggers
  (SQLite does not support multi-column CHECK constraints across rows without triggers;
  this is a known design limitation, documented in `defect_log.csv`)
- The `eligible` field is a simplified flag (0/1) and does not represent any real-world
  eligibility determination process

---

## Architecture

```
CSV fixtures (data/)
        │
        ▼
setup_db.py  ──► benefits_enrollment.db  (SQLite)
        │
        ▼
sql_validations.sql  (manual SQL checks)
        │
        ▼
tests/  (pytest — uses isolated tmp_path databases)
```

- **SQLite** is used as the database engine. It requires no separate server.
- **pytest** creates a fresh temporary database for each test, so tests are
  completely isolated from each other and from the main database.
- **CSV files** in `data/` are the single source of truth for test fixtures.
  `setup_db.py` reads them to populate the live database.

---

## Project Structure

```
employee-benefits-qa/
├── .gitignore                     ← git ignore rules
├── README.md                      ← this file
├── requirements.txt               ← Python dependencies (pytest, python-docx)
├── schema.sql                     ← database table definitions
├── setup_db.py                    ← initialise / reset the database
├── sql_validations.sql            ← 19 documented SQL validation queries
├── run_sql_checks.py              ← runs all 19 VQ checks via Python
├── verify_negative_fixtures.py    ← confirms all invalid fixtures are detected
├── generate_report.py             ← regenerates Project_Report.docx
├── Project_Report.docx            ← professional project report (10 sections)
├── data/
│   ├── employees.csv              ← 12 baseline employees (valid)
│   ├── benefit_plans.csv          ← 8 baseline plans (valid)
│   ├── dependents.csv             ← 7 baseline dependents (valid)
│   ├── enrollments.csv            ← 14 baseline enrollments (valid)
│   ├── invalid_employees.csv      ← 6 intentionally invalid employee rows
│   ├── invalid_plans.csv          ← 4 intentionally invalid plan rows
│   └── invalid_enrollments.csv    ← 10 intentionally invalid enrollment rows
├── tests/
│   ├── __init__.py
│   ├── conftest.py                ← shared pytest fixtures (isolated tmp_path DBs)
│   ├── test_enrollment.py         ← 14 enrollment tests (TC-E01 to TC-E14)
│   ├── test_employees.py          ←  9 employee tests (TC-EMP01 to TC-EMP09)
│   ├── test_plans.py              ← 10 plan tests (TC-P01 to TC-P10)
│   ├── test_constraints.py        ← 11 constraint/FK tests (TC-C01 to TC-C11)
│   └── test_sql_validations.py    ← 19 SQL validation tests (TC-SV01 to TC-SV19)
├── test_cases.csv                 ← 63 test case records
├── defect_log.csv                 ← illustrative defect examples
└── test_execution_report.md       ← real test execution results
```

---

## Business Rules

All rules are simplified educational assumptions.  No real jurisdiction rules apply.

| ID    | Rule | Enforced by |
|-------|------|-------------|
| BR-01 | `employee_id`, `plan_id`, `enrollment_id`, `dependent_id` are mandatory and unique | DB PRIMARY KEY |
| BR-02 | Enrollment must reference a real `employee_id` | DB FOREIGN KEY |
| BR-03 | Enrollment must reference a real `plan_id` | DB FOREIGN KEY |
| BR-04 | Only `ACTIVE` employees with `eligible=1` may hold `APPROVED` enrollments | SQL check (VQ-13, VQ-14) |
| BR-05 | Plan `end_date` must be strictly after `effective_date` when present | DB CHECK constraint |
| BR-06 | `enrollment_date` must be ≥ employee `hire_date` | SQL check (VQ-16) |
| BR-07 | `coverage_start` must be ≥ `enrollment_date` | SQL check (VQ-17) |
| BR-08 | No duplicate APPROVED enrollment for the same employee+plan | SQL check (VQ-09) |
| BR-09 | Enrollment `status` must be `APPROVED`, `PENDING`, or `CANCELLED` | DB CHECK constraint |
| BR-10 | Dependent must reference a real `employee_id` | DB FOREIGN KEY |

**Why some rules use SQL checks instead of DB constraints:**
SQLite CHECK constraints cannot reference other rows or tables.  Rules like BR-04
(join employees to check status + eligible) and BR-08 (count rows for
duplicate detection) require either application code, a trigger, or a SQL
validation query.  This project uses SQL validation queries, which is the
standard approach in many HW/benefits data warehouse contexts.

---

## Setup Instructions

### Prerequisites

- Python 3.9 or later (check: `python --version`)
- pip (comes with Python)
- SQLite (bundled with Python — no separate install needed)

### Step 1 — Create and activate a virtual environment (Windows PowerShell)

```powershell
# Navigate to the project folder
cd "C:\path\to\employee-benefits-qa"

# Create the virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1
```

> **If you see "execution of scripts is disabled"**, run this once in an
> administrator PowerShell session:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

You should now see `(venv)` at the start of your prompt.

### Step 2 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3 — Initialise the database

```powershell
python setup_db.py
```

This creates `benefits_enrollment.db` and loads all baseline CSV files.
Run it again at any time to reset the database to a clean state.

---

## Running SQL Validations

```powershell
sqlite3 benefits_enrollment.db ".read sql_validations.sql"
```

**Expected result on clean baseline data:** every query (VQ-01 through VQ-18)
returns 0 rows.  VQ-19 returns the row-count summary:
`employees=12, benefit_plans=8, dependents=7, enrollments=14`.

> If `sqlite3` is not on your PATH, download it from
> https://www.sqlite.org/download.html and add it to your PATH, or use
> the Python REPL: `python -c "import sqlite3; ..."`.

---

## Running Tests

```powershell
# Run all tests with verbose output
pytest tests/ -v

# Run a specific test file
pytest tests/test_enrollment.py -v

# Run a specific test by name
pytest tests/test_enrollment.py::test_valid_enrollment_inserted -v

# Stop on the first failure
pytest tests/ -v -x
```

Tests use temporary databases in `tmp_path` so they never touch
`benefits_enrollment.db`.  You do **not** need to run `setup_db.py`
before running tests.

---

## Test Data Overview

### Baseline employees (data/employees.csv)

| Employee ID | Name | Status | Eligible | Notes |
|-------------|------|--------|----------|-------|
| EMP001 | Alice Nguyen | ACTIVE | 1 | Normal eligible employee |
| EMP002 | Bob Okafor | ACTIVE | 1 | Normal eligible employee |
| EMP003 | Carol Patel | ACTIVE | 1 | Normal eligible employee |
| EMP004 | David Martinez | INACTIVE | 0 | Inactive — must not get APPROVED |
| EMP005 | Eva Lindqvist | TERMINATED | 0 | Terminated — must not get APPROVED |
| EMP006 | Frank Osei | ACTIVE | 1 | New hire edge case |
| EMP007 | Grace Yamamoto | ACTIVE | 1 | Recent hire |
| EMP008 | Henry Dubois | ACTIVE | 1 | Long-tenure employee |
| EMP009 | Irene Castillo | INACTIVE | 0 | Inactive edge case |
| EMP010 | James Khoury | ACTIVE | 1 | Very recent hire (2024) |
| EMP011 | Karen Obi | ACTIVE | 1 | Multi-plan employee |
| EMP012 | Leo Ferreira | ACTIVE | 0 | Active but ineligible (eligible=0) |

### Invalid fixtures (NOT loaded into the main database)

The files `invalid_employees.csv`, `invalid_plans.csv`, and
`invalid_enrollments.csv` contain intentionally bad records with a `test_note`
column explaining each violation.  These are used only in pytest tests to verify
that the system correctly rejects or flags bad data.  They are **not** loaded
by `setup_db.py`.

---

## Key Commands Reference

| Task | Command |
|------|---------|
| Activate venv | `venv\Scripts\Activate.ps1` |
| Install deps | `pip install -r requirements.txt` |
| Init / reset DB | `python setup_db.py` |
| Run SQL checks | `python run_sql_checks.py` |
| Verify negative fixtures | `python verify_negative_fixtures.py` |
| Run all tests | `pytest tests/ -v` |
| Run one test file | `pytest tests/test_enrollment.py -v` |
| Regenerate report | `python generate_report.py` |
| Deactivate venv | `deactivate` |

---

## Uploading to GitHub

```powershell
# 1. Initialise git (run from inside the employee-benefits-qa/ folder)
git init
git add .
git commit -m "Initial commit: Employee Benefits Enrollment QA project"

# 2. Create a new empty repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/employee-benefits-qa.git
git branch -M main
git push -u origin main
```

> Do **not** commit `benefits_enrollment.db` — it is excluded by `.gitignore`
> and can always be regenerated with `python setup_db.py`.
