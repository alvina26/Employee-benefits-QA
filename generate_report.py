"""
generate_report.py
==================
Generates Project_Report.docx using python-docx.
Run: python generate_report.py

This script creates a professional project report for the
Employee Benefits Enrollment QA Validation portfolio project.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

OUTPUT = Path(__file__).parent / "Project_Report.docx"


def set_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    return h


def add_para(doc, text, size=11, bold=False, italic=False, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p


def add_bullet(doc, text, size=11):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    for run in p.runs:
        run.font.size = Pt(size)
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Add a styled table with bold header row."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"

    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        run = hdr_cells[i].paragraphs[0].runs[0]
        run.bold = True
        run.font.size = Pt(10)
        # Blue background
        shading = OxmlElement("w:shd")
        shading.set(qn("w:val"), "clear")
        shading.set(qn("w:color"), "auto")
        shading.set(qn("w:fill"), "2F5496")
        hdr_cells[i].paragraphs[0]._p.get_or_add_pPr().append(shading)
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, cell_text in enumerate(row_data):
            row_cells[c_idx].text = str(cell_text)
            for run in row_cells[c_idx].paragraphs[0].runs:
                run.font.size = Pt(9)

    if col_widths:
        for i, width in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(width)

    doc.add_paragraph()  # spacing after table
    return table


def main():
    doc = Document()

    # ----------------------------------------------------------------
    # Page margins
    # ----------------------------------------------------------------
    section = doc.sections[0]
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

    # ----------------------------------------------------------------
    # Title
    # ----------------------------------------------------------------
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(4)
    r = title.add_run("Employee Benefits Enrollment — QA Validation")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(31, 67, 120)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.paragraph_format.space_after = Pt(4)
    r2 = sub.add_run("Portfolio Project Report  |  Graduate Engineer Trainee — HW Technology")
    r2.font.size = Pt(12)
    r2.italic = True
    r2.font.color.rgb = RGBColor(87, 96, 106)

    notice = doc.add_paragraph()
    notice.alignment = WD_ALIGN_PARAGRAPH.CENTER
    notice.paragraph_format.space_after = Pt(20)
    r3 = notice.add_run(
        "SIMULATED LEARNING PROJECT  |  All data is fictional  |  "
        "Not professional healthcare or insurance advice"
    )
    r3.font.size = Pt(9)
    r3.font.color.rgb = RGBColor(150, 50, 50)

    # ----------------------------------------------------------------
    # Section 1: Objectives
    # ----------------------------------------------------------------
    set_heading(doc, "1. Project Objectives")
    add_para(doc, (
        "This project demonstrates foundational QA engineering skills relevant to a "
        "Graduate Engineer Trainee role in Health and Welfare (HW) Technology. "
        "The simulated system models an Employee Benefits Enrollment process, providing "
        "a realistic context for applying data validation, SQL checks, and automated "
        "testing techniques without using any real personal, financial, or health data."
    ))
    add_para(doc, "Key learning objectives:", bold=True)
    for item in [
        "Test data preparation — valid baseline and intentionally invalid CSV fixtures",
        "Database schema design using SQLite with PRIMARY KEY, FOREIGN KEY, and CHECK constraints",
        "SQL-based data quality validation with 19 documented VQ checks",
        "Automated pytest testing — 63 tests covering positive and negative scenarios",
        "QA documentation — test cases, defect log, and real test execution reporting",
    ]:
        add_bullet(doc, item)

    # ----------------------------------------------------------------
    # Section 2: Requirements & Business Rules
    # ----------------------------------------------------------------
    set_heading(doc, "2. Requirements and Business Rules")
    add_para(doc, (
        "Ten business rules were defined before implementation to guide the schema design, "
        "test data creation, SQL validation queries, and automated tests. "
        "All rules are simplified educational assumptions and do not represent any "
        "jurisdiction-specific insurance, regulatory, or compliance requirement."
    ))

    br_headers = ["Rule ID", "Description", "Enforcement Mechanism"]
    br_rows = [
        ["BR-01", "All primary keys (employee_id, plan_id, enrollment_id, dependent_id) are mandatory and unique", "DB PRIMARY KEY"],
        ["BR-02", "Enrollment must reference an existing employee_id", "DB FOREIGN KEY"],
        ["BR-03", "Enrollment must reference an existing plan_id", "DB FOREIGN KEY"],
        ["BR-04", "Only ACTIVE employees with eligible=1 may hold APPROVED enrollments", "SQL checks VQ-13, VQ-14"],
        ["BR-05", "Plan end_date must be strictly after effective_date when present", "DB CHECK constraint"],
        ["BR-06", "enrollment_date must be on or after employee hire_date", "SQL check VQ-16"],
        ["BR-07", "coverage_start must be on or after enrollment_date", "SQL check VQ-17"],
        ["BR-08", "No duplicate APPROVED enrollment for same employee+plan", "SQL check VQ-09"],
        ["BR-09", "Enrollment status must be APPROVED, PENDING, or CANCELLED", "DB CHECK constraint"],
        ["BR-10", "Dependent must reference an existing employee_id", "DB FOREIGN KEY"],
    ]
    add_table(doc, br_headers, br_rows, col_widths=[0.8, 3.8, 1.8])

    # ----------------------------------------------------------------
    # Section 3: System Design
    # ----------------------------------------------------------------
    set_heading(doc, "3. System Design and Architecture")
    add_para(doc, "The project uses the following technology stack:")
    for item in [
        "Python 3.12 — application logic, setup script, test code",
        "SQLite 3 — embedded database, no server required",
        "pytest 9.1 — automated test framework",
        "python-docx — report generation (this document)",
        "CSV files — single source of truth for test fixtures",
    ]:
        add_bullet(doc, item)

    add_para(doc, "Database tables:", bold=True)
    tbl_headers = ["Table", "Purpose", "Key Columns"]
    tbl_rows = [
        ["employees", "Stores fictional employee records", "employee_id (PK), employment_status, hire_date, eligible"],
        ["benefit_plans", "Stores fictional benefit plan definitions", "plan_id (PK), plan_type, effective_date, end_date"],
        ["dependents", "Optional: dependents linked to employees", "dependent_id (PK), employee_id (FK), relationship"],
        ["enrollments", "Records employee-plan enrollment events", "enrollment_id (PK), employee_id (FK), plan_id (FK), status"],
    ]
    add_table(doc, tbl_headers, tbl_rows, col_widths=[1.2, 2.5, 2.7])

    add_para(doc, (
        "Test isolation is achieved through pytest's built-in tmp_path fixture. "
        "Each test receives its own fresh temporary SQLite database, ensuring that "
        "tests cannot interfere with each other and the main benefits_enrollment.db "
        "is never touched during test execution."
    ))

    # ----------------------------------------------------------------
    # Section 4: Test Data
    # ----------------------------------------------------------------
    set_heading(doc, "4. Test Data Overview")
    add_para(doc, (
        "Separate valid (baseline) and invalid (negative-test) datasets were created. "
        "The baseline data is loaded by setup_db.py into the main database. "
        "The invalid fixtures are used only within pytest tests and are never loaded "
        "into the production database."
    ))

    emp_headers = ["Employee ID", "Name", "Status", "Eligible", "Test Purpose"]
    emp_rows = [
        ["EMP001", "Alice Nguyen",    "ACTIVE",     "1", "Standard eligible employee"],
        ["EMP002", "Bob Okafor",      "ACTIVE",     "1", "Multi-plan enrollment"],
        ["EMP003", "Carol Patel",     "ACTIVE",     "1", "Transfer enrollment"],
        ["EMP004", "David Martinez",  "INACTIVE",   "0", "BR-04 negative test"],
        ["EMP005", "Eva Lindqvist",   "TERMINATED", "0", "BR-04 negative test"],
        ["EMP006", "Frank Osei",      "ACTIVE",     "1", "New hire edge case"],
        ["EMP007", "Grace Yamamoto",  "ACTIVE",     "1", "Recent hire"],
        ["EMP008", "Henry Dubois",    "ACTIVE",     "1", "Long-tenure employee"],
        ["EMP009", "Irene Castillo",  "INACTIVE",   "0", "INACTIVE edge case"],
        ["EMP010", "James Khoury",    "ACTIVE",     "1", "Very recent hire (2024)"],
        ["EMP011", "Karen Obi",       "ACTIVE",     "1", "Multiple approved enrollments"],
        ["EMP012", "Leo Ferreira",    "ACTIVE",     "0", "Active but ineligible (eligible=0)"],
    ]
    add_table(doc, emp_headers, emp_rows, col_widths=[0.9, 1.4, 1.0, 0.8, 2.3])

    add_para(doc, (
        "Invalid fixture files (invalid_employees.csv, invalid_plans.csv, "
        "invalid_enrollments.csv) each contain a test_note column explaining "
        "which business rule each intentionally bad row violates."
    ))

    # ----------------------------------------------------------------
    # Section 5: SQL Validations
    # ----------------------------------------------------------------
    set_heading(doc, "5. SQL Validation Queries")
    add_para(doc, (
        "sql_validations.sql contains 19 documented SQL validation queries (VQ-01 through "
        "VQ-19) grouped into six categories. All 19 return 0 rows when run against the "
        "valid baseline data, confirming the baseline dataset is clean."
    ))
    vq_headers = ["Check ID", "Category", "What It Detects"]
    vq_rows = [
        ["VQ-01 to VQ-05",  "Missing required values",       "NULL primary keys, hire_date, enrollment fields"],
        ["VQ-06 to VQ-09",  "Duplicate identifiers",         "Dup employee_id, plan_id, enrollment_id; dup APPROVED enrollments"],
        ["VQ-10 to VQ-12",  "Orphaned FK references",        "Enrollments or dependents with no matching employee or plan"],
        ["VQ-13 to VQ-14",  "Eligibility violations",        "APPROVED enrollments for INACTIVE, TERMINATED, or ineligible employees"],
        ["VQ-15 to VQ-17",  "Invalid date ranges",           "Plan dates backwards; enrollment before hire; coverage before enrollment"],
        ["VQ-18",           "Invalid status values",         "Status values outside the allowed APPROVED/PENDING/CANCELLED set"],
        ["VQ-19",           "Row-count summary (info only)", "Baseline counts: 12 employees, 8 plans, 7 dependents, 14 enrollments"],
    ]
    add_table(doc, vq_headers, vq_rows, col_widths=[1.3, 1.8, 3.3])

    # ----------------------------------------------------------------
    # Section 6: Automated Tests
    # ----------------------------------------------------------------
    set_heading(doc, "6. Automated Test Design")
    add_para(doc, (
        "63 pytest tests are organised across five test files. "
        "Each test has a meaningful assertion (not just 'no exception was raised') and "
        "maps to a documented test case in test_cases.csv."
    ))
    test_headers = ["File", "Tests", "Coverage Area"]
    test_rows = [
        ["test_employees.py",       "9",  "Employee record validation, PK constraints, CHECK constraints"],
        ["test_plans.py",           "10", "Benefit plan validation, date rules (BR-05), PK/CHECK constraints"],
        ["test_enrollment.py",      "14", "Enrollment business rules BR-02 through BR-09"],
        ["test_constraints.py",     "11", "FK integrity, DELETE blocking, dependent constraints"],
        ["test_sql_validations.py", "19", "All 19 VQ SQL checks against baseline data"],
    ]
    add_table(doc, test_headers, test_rows, col_widths=[2.0, 0.7, 3.7])

    # ----------------------------------------------------------------
    # Section 7: Test Execution Results
    # ----------------------------------------------------------------
    set_heading(doc, "7. Test Execution Results")
    add_para(doc, (
        "Tests were executed on 2025-07-12 using the command: pytest tests/ -v"
    ))
    result_headers = ["Metric", "Value"]
    result_rows = [
        ["Date",             "2025-07-12"],
        ["Python version",   "3.12.4"],
        ["pytest version",   "9.1.1"],
        ["Platform",         "Windows 10 (win32)"],
        ["Tests collected",  "63"],
        ["Passed",           "63"],
        ["Failed",           "0"],
        ["Errors",           "0"],
        ["Duration",         "10.74 seconds"],
        ["Overall result",   "ALL TESTS PASSED"],
    ]
    add_table(doc, result_headers, result_rows, col_widths=[2.0, 4.4])

    add_para(doc, (
        "One non-functional issue was encountered and resolved during setup: "
        "setup_db.py used a Unicode arrow character (U+2192) in a print statement "
        "that could not be encoded by the Windows cp1252 console. "
        "This was fixed by replacing it with the ASCII '->' sequence. "
        "No test logic or data was changed."
    ))

    # ----------------------------------------------------------------
    # Section 8: Defects and Design Limitations
    # ----------------------------------------------------------------
    set_heading(doc, "8. Design Limitations and Known Gaps")
    add_para(doc, (
        "Two design notes are recorded in defect_log.csv as clearly marked illustrative "
        "examples. These are intentional design trade-offs, not application defects:"
    ))
    for item in [
        "DEF-ILLUSTRATIVE-01: BR-04 (employment status and eligibility check) is not "
        "enforced at the database INSERT level. SQLite CHECK constraints cannot join "
        "tables. The rule is validated by SQL queries VQ-13 and VQ-14 and by "
        "tests TC-E06, TC-E07, and TC-E11. A DB trigger could enforce this if needed.",

        "DEF-ILLUSTRATIVE-02: BR-08 (duplicate APPROVED enrollment for same employee+plan) "
        "is not blocked at INSERT time. A UNIQUE constraint on (employee_id, plan_id, status) "
        "would enforce this but was intentionally omitted to keep the schema simple for this "
        "educational project. VQ-09 and test TC-E03 detect the violation after the fact.",
    ]:
        add_bullet(doc, item)

    add_para(doc, (
        "Additional limitations: dates are stored as TEXT in ISO-8601 format (YYYY-MM-DD); "
        "no web UI or REST API is included; no concurrent access testing was performed; "
        "no real personal or health data is used anywhere in the project."
    ))

    # ----------------------------------------------------------------
    # Section 9: Future Improvements
    # ----------------------------------------------------------------
    set_heading(doc, "9. Future Improvements")
    for item in [
        "Add DB triggers to enforce BR-04 and BR-08 at the INSERT level",
        "Introduce a UNIQUE constraint on (employee_id, plan_id) within APPROVED status",
        "Add a REST API layer (Flask or FastAPI) to expose enrollment operations",
        "Expand the test suite with property-based testing (Hypothesis library)",
        "Add a CI/CD pipeline (GitHub Actions) to run pytest on every push",
        "Extend the schema with a plan_tier or benefit_amount table for richer rules",
        "Generate an HTML test report using pytest-html for easier review sharing",
    ]:
        add_bullet(doc, item)

    # ----------------------------------------------------------------
    # Section 10: How to Run
    # ----------------------------------------------------------------
    set_heading(doc, "10. How to Run This Project")
    cmd_headers = ["Step", "Command", "Purpose"]
    cmd_rows = [
        ["1", "python -m venv venv", "Create Python virtual environment"],
        ["2", r"venv\Scripts\Activate.ps1", "Activate venv (Windows PowerShell)"],
        ["3", "pip install -r requirements.txt", "Install pytest and python-docx"],
        ["4", "python setup_db.py", "Create and populate the SQLite database"],
        ["5", 'sqlite3 benefits_enrollment.db ".read sql_validations.sql"', "Run SQL validations"],
        ["6", "pytest tests/ -v", "Run the full test suite"],
        ["7", "python generate_report.py", "Regenerate this report"],
    ]
    add_table(doc, cmd_headers, cmd_rows, col_widths=[0.4, 2.8, 2.8])

    # ----------------------------------------------------------------
    # Footer / metadata
    # ----------------------------------------------------------------
    doc.add_paragraph()
    footer_p = doc.add_paragraph()
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.space_before = Pt(20)
    r_footer = footer_p.add_run(
        f"Generated {datetime.date.today().isoformat()}  |  "
        "Simulated Learning Project — Employee Benefits Enrollment QA Validation  |  "
        "All data is fictional"
    )
    r_footer.font.size = Pt(8)
    r_footer.font.color.rgb = RGBColor(130, 130, 130)
    r_footer.italic = True

    doc.save(str(OUTPUT))
    print(f"[OK] Project_Report.docx written to {OUTPUT}")


if __name__ == "__main__":
    main()
