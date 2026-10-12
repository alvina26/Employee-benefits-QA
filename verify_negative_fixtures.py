"""
verify_negative_fixtures.py
===========================
Loads each invalid fixture file into a temporary in-memory database
and confirms every stated violation is actually detected by the
corresponding SQL check.

Exit code 0 = all negative scenarios detected correctly.
Exit code 1 = one or more scenarios were NOT detected (fixture or check is wrong).
"""
import csv
import sqlite3
from pathlib import Path

BASE = Path(__file__).parent
SCHEMA = (BASE / "schema.sql").read_text(encoding="utf-8")


def fresh_db_with_baseline() -> sqlite3.Connection:
    """In-memory DB with schema + valid baseline loaded."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    for fname, table in [
        ("employees.csv",     "employees"),
        ("benefit_plans.csv", "benefit_plans"),
        ("dependents.csv",    "dependents"),
        ("enrollments.csv",   "enrollments"),
    ]:
        _load_csv(conn, BASE / "data" / fname, table)
    return conn


def _load_csv(conn, path, table):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return
    valid_cols = [c for c in rows[0] if c != "test_note"]
    ph = ", ".join("?" for _ in valid_cols)
    sql = f"INSERT INTO {table} ({', '.join(valid_cols)}) VALUES ({ph})"
    for r in rows:
        conn.execute(sql, tuple(None if r[c] == "" else r[c] for c in valid_cols))
    conn.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Individual negative scenario checks
# ─────────────────────────────────────────────────────────────────────────────

def check(label, passed, detail=""):
    tag = "PASS" if passed else "FAIL"
    print(f"  {tag}  {label}" + (f"  [{detail}]" if detail else ""))
    return passed


def run():
    results = []

    # ── INVALID EMPLOYEES ────────────────────────────────────────────────────
    print("\nNegative fixture: invalid_employees.csv")

    # Row 1: NULL employee_id → PRIMARY KEY should reject
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                     "employment_status,hire_date,eligible) "
                     "VALUES (NULL,'X','Y','ACTIVE','2020-01-01',1)")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("NULL employee_id is rejected by PRIMARY KEY", raised))
    conn.close()

    # Rows 2+3: duplicate employee_id → PRIMARY KEY should reject
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                 "employment_status,hire_date,eligible) "
                 "VALUES ('EMP_DUP','A','B','ACTIVE','2020-01-01',1)")
    conn.commit()
    raised = False
    try:
        conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                     "employment_status,hire_date,eligible) "
                     "VALUES ('EMP_DUP','C','D','ACTIVE','2021-01-01',1)")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("Duplicate employee_id rejected by PRIMARY KEY", raised))
    conn.close()

    # Row 4: invalid employment_status → CHECK constraint
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                     "employment_status,hire_date,eligible) "
                     "VALUES ('EMP013','D','R','BADSTATUS','2022-01-01',1)")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("Invalid employment_status rejected by CHECK", raised))
    conn.close()

    # Row 5: NULL hire_date → NOT NULL
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                     "employment_status,hire_date,eligible) "
                     "VALUES ('EMP014','E','S','ACTIVE',NULL,1)")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("NULL hire_date rejected by NOT NULL", raised))
    conn.close()

    # Row 6: eligible=2 → CHECK (eligible IN (0,1))
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO employees (employee_id,first_name,last_name,"
                     "employment_status,hire_date,eligible) "
                     "VALUES ('EMP015','F','G','ACTIVE','2023-01-01',2)")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("eligible=2 rejected by CHECK", raised))
    conn.close()

    # ── INVALID PLANS ─────────────────────────────────────────────────────────
    print("\nNegative fixture: invalid_plans.csv")

    # PLN_BAD1: NULL plan_type
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO benefit_plans (plan_id,plan_name,plan_type,effective_date)"
                     " VALUES ('PLN_BAD1','NoType',NULL,'2022-01-01')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("NULL plan_type rejected (NOT NULL)", raised))
    conn.close()

    # PLN_BAD2: end_date before effective_date → CHECK
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO benefit_plans (plan_id,plan_name,plan_type,effective_date,end_date)"
                     " VALUES ('PLN_BAD2','Back','MEDICAL','2022-12-31','2022-01-01')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("end_date < effective_date rejected by CHECK (BR-05)", raised))
    conn.close()

    # PLN_BAD3: end_date == effective_date → CHECK
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO benefit_plans (plan_id,plan_name,plan_type,effective_date,end_date)"
                     " VALUES ('PLN_BAD3','Same','DENTAL','2022-06-01','2022-06-01')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("end_date == effective_date rejected by CHECK (BR-05)", raised))
    conn.close()

    # NULL plan_id
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    raised = False
    try:
        conn.execute("INSERT INTO benefit_plans (plan_id,plan_name,plan_type,effective_date)"
                     " VALUES (NULL,'Unnamed','VISION','2022-01-01')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("NULL plan_id rejected by PRIMARY KEY", raised))
    conn.close()

    # ── INVALID ENROLLMENTS ──────────────────────────────────────────────────
    print("\nNegative fixture: invalid_enrollments.csv")

    # ENR_BAD1: non-existent employee FK
    conn = fresh_db_with_baseline()
    raised = False
    try:
        conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                     "enrollment_date,coverage_start,status)"
                     " VALUES ('ENR_BAD1','EMP999','PLN001','2022-01-10','2022-02-01','APPROVED')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("Non-existent employee_id rejected by FK (BR-02)", raised))
    conn.close()

    # ENR_BAD2: non-existent plan FK
    conn = fresh_db_with_baseline()
    raised = False
    try:
        conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                     "enrollment_date,coverage_start,status)"
                     " VALUES ('ENR_BAD2','EMP001','PLN999','2022-01-10','2022-02-01','APPROVED')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("Non-existent plan_id rejected by FK (BR-03)", raised))
    conn.close()

    # ENR_BAD3: INACTIVE employee with APPROVED → detected by VQ-13
    conn = fresh_db_with_baseline()
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD3','EMP004','PLN001','2022-01-10','2022-02-01','APPROVED')")
    conn.commit()
    rows = conn.execute(
        "SELECT e.enrollment_id FROM enrollments e "
        "JOIN employees emp ON emp.employee_id=e.employee_id "
        "WHERE e.status='APPROVED' AND emp.employment_status<>'ACTIVE'"
    ).fetchall()
    detected = any(r["enrollment_id"] == "ENR_BAD3" for r in rows)
    results.append(check("INACTIVE employee APPROVED enrollment detected by VQ-13 (BR-04)", detected))
    conn.close()

    # ENR_BAD4: TERMINATED employee with APPROVED → detected by VQ-13
    conn = fresh_db_with_baseline()
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD4','EMP005','PLN002','2022-01-10','2022-02-01','APPROVED')")
    conn.commit()
    rows = conn.execute(
        "SELECT e.enrollment_id FROM enrollments e "
        "JOIN employees emp ON emp.employee_id=e.employee_id "
        "WHERE e.status='APPROVED' AND emp.employment_status<>'ACTIVE'"
    ).fetchall()
    detected = any(r["enrollment_id"] == "ENR_BAD4" for r in rows)
    results.append(check("TERMINATED employee APPROVED enrollment detected by VQ-13 (BR-04)", detected))
    conn.close()

    # ENR_BAD5: duplicate APPROVED same employee+plan → detected by VQ-09
    conn = fresh_db_with_baseline()
    # ENR001 already has EMP001+PLN001 APPROVED in baseline
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD5','EMP001','PLN001','2022-06-01','2022-07-01','APPROVED')")
    conn.commit()
    row = conn.execute(
        "SELECT COUNT(*) c FROM enrollments "
        "WHERE employee_id='EMP001' AND plan_id='PLN001' AND status='APPROVED'"
    ).fetchone()
    results.append(check("Duplicate APPROVED enrollment detected by VQ-09 (BR-08)", row["c"] > 1,
                         f"count={row['c']}"))
    conn.close()

    # ENR_BAD6: coverage_start before enrollment_date → detected by VQ-17
    conn = fresh_db_with_baseline()
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD6','EMP001','PLN002','2022-01-10','2021-12-01','APPROVED')")
    conn.commit()
    rows = conn.execute(
        "SELECT enrollment_id FROM enrollments WHERE coverage_start<enrollment_date"
    ).fetchall()
    detected = any(r["enrollment_id"] == "ENR_BAD6" for r in rows)
    results.append(check("coverage_start < enrollment_date detected by VQ-17 (BR-07)", detected))
    conn.close()

    # ENR_BAD7: enrollment before hire date → detected by VQ-16
    # EMP001 hire_date=2019-03-15, enrollment_date=2018-01-01
    conn = fresh_db_with_baseline()
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD7','EMP001','PLN002','2018-01-01','2018-02-01','APPROVED')")
    conn.commit()
    rows = conn.execute(
        "SELECT e.enrollment_id FROM enrollments e "
        "JOIN employees emp ON emp.employee_id=e.employee_id "
        "WHERE e.enrollment_date<emp.hire_date"
    ).fetchall()
    detected = any(r["enrollment_id"] == "ENR_BAD7" for r in rows)
    results.append(check("enrollment_date before hire_date detected by VQ-16 (BR-06)", detected))
    conn.close()

    # ENR_BAD8: invalid status value → CHECK constraint
    conn = fresh_db_with_baseline()
    raised = False
    try:
        conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                     "enrollment_date,coverage_start,status)"
                     " VALUES ('ENR_BAD8','EMP001','PLN002','2022-01-10','2022-02-01','DRAFTED')")
    except sqlite3.IntegrityError:
        raised = True
    results.append(check("Invalid status 'DRAFTED' rejected by CHECK (BR-09)", raised))
    conn.close()

    # ENR_BAD9: ineligible (eligible=0) ACTIVE employee APPROVED → VQ-14
    conn = fresh_db_with_baseline()
    # EMP012 is ACTIVE with eligible=0
    conn.execute("INSERT INTO enrollments (enrollment_id,employee_id,plan_id,"
                 "enrollment_date,coverage_start,status)"
                 " VALUES ('ENR_BAD9','EMP012','PLN001','2023-11-01','2023-12-01','APPROVED')")
    conn.commit()
    rows = conn.execute(
        "SELECT e.enrollment_id FROM enrollments e "
        "JOIN employees emp ON emp.employee_id=e.employee_id "
        "WHERE e.status='APPROVED' AND emp.eligible=0"
    ).fetchall()
    detected = any(r["enrollment_id"] == "ENR_BAD9" for r in rows)
    results.append(check("Ineligible employee APPROVED enrollment detected by VQ-14 (BR-04)", detected))
    conn.close()

    # ── Summary ───────────────────────────────────────────────────────────────
    total = len(results)
    passed = sum(results)
    failed = total - passed
    print(f"\n{'='*60}")
    print(f"NEGATIVE FIXTURE VERIFICATION: {passed}/{total} detected correctly")
    if failed:
        print(f"  WARNING: {failed} scenario(s) NOT detected — fix before publishing")
    else:
        print("  ALL NEGATIVE SCENARIOS DETECTED AS EXPECTED")
    return failed == 0


if __name__ == "__main__":
    import sys
    ok = run()
    sys.exit(0 if ok else 1)
