"""
run_sql_checks.py  –  execute all 19 VQ checks against benefits_enrollment.db
and print a pass/fail summary.  Used during pre-publication review.
"""
import sqlite3

DB = "benefits_enrollment.db"

CHECKS = {
    "VQ-01 NULL employee_id":
        "SELECT employee_id FROM employees WHERE employee_id IS NULL OR TRIM(employee_id)=''",
    "VQ-02 NULL hire_date":
        "SELECT employee_id FROM employees WHERE hire_date IS NULL OR TRIM(hire_date)=''",
    "VQ-03 NULL plan_id":
        "SELECT plan_id FROM benefit_plans WHERE plan_id IS NULL OR TRIM(plan_id)=''",
    "VQ-04 NULL enrollment_id":
        "SELECT enrollment_id FROM enrollments WHERE enrollment_id IS NULL OR TRIM(enrollment_id)=''",
    "VQ-05 missing enrollment fields":
        ("SELECT enrollment_id FROM enrollments "
         "WHERE employee_id IS NULL OR plan_id IS NULL "
         "OR enrollment_date IS NULL OR coverage_start IS NULL OR status IS NULL"),
    "VQ-06 dup employee_id":
        "SELECT employee_id, COUNT(*) c FROM employees GROUP BY employee_id HAVING c>1",
    "VQ-07 dup plan_id":
        "SELECT plan_id, COUNT(*) c FROM benefit_plans GROUP BY plan_id HAVING c>1",
    "VQ-08 dup enrollment_id":
        "SELECT enrollment_id, COUNT(*) c FROM enrollments GROUP BY enrollment_id HAVING c>1",
    "VQ-09 dup APPROVED same emp+plan":
        ("SELECT employee_id, plan_id, COUNT(*) c FROM enrollments "
         "WHERE status='APPROVED' GROUP BY employee_id, plan_id HAVING c>1"),
    "VQ-10 orphaned enrollment->employee":
        ("SELECT enrollment_id FROM enrollments e "
         "WHERE NOT EXISTS(SELECT 1 FROM employees x WHERE x.employee_id=e.employee_id)"),
    "VQ-11 orphaned enrollment->plan":
        ("SELECT enrollment_id FROM enrollments e "
         "WHERE NOT EXISTS(SELECT 1 FROM benefit_plans p WHERE p.plan_id=e.plan_id)"),
    "VQ-12 orphaned dependent->employee":
        ("SELECT dependent_id FROM dependents d "
         "WHERE NOT EXISTS(SELECT 1 FROM employees e WHERE e.employee_id=d.employee_id)"),
    "VQ-13 APPROVED for non-ACTIVE emp":
        ("SELECT e.enrollment_id FROM enrollments e "
         "JOIN employees emp ON emp.employee_id=e.employee_id "
         "WHERE e.status='APPROVED' AND emp.employment_status<>'ACTIVE'"),
    "VQ-14 APPROVED for ineligible emp":
        ("SELECT e.enrollment_id FROM enrollments e "
         "JOIN employees emp ON emp.employee_id=e.employee_id "
         "WHERE e.status='APPROVED' AND emp.eligible=0"),
    "VQ-15 plan end<=effective":
        ("SELECT plan_id FROM benefit_plans "
         "WHERE end_date IS NOT NULL AND end_date<=effective_date"),
    "VQ-16 enrollment before hire":
        ("SELECT e.enrollment_id FROM enrollments e "
         "JOIN employees emp ON emp.employee_id=e.employee_id "
         "WHERE e.enrollment_date<emp.hire_date"),
    "VQ-17 coverage before enrollment":
        "SELECT enrollment_id FROM enrollments WHERE coverage_start<enrollment_date",
    "VQ-18 invalid status":
        ("SELECT enrollment_id FROM enrollments "
         "WHERE status NOT IN ('APPROVED','PENDING','CANCELLED')"),
}

EXPECTED_COUNTS = {
    "employees": 12,
    "benefit_plans": 8,
    "dependents": 7,
    "enrollments": 14,
}


def run():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row

    print(f"\nSQL Validation Results against {DB}")
    print("=" * 60)

    all_ok = True
    for name, sql in CHECKS.items():
        rows = db.execute(sql).fetchall()
        ok = len(rows) == 0
        tag = "PASS (0 rows)" if ok else f"FAIL ({len(rows)} rows)"
        if not ok:
            all_ok = False
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")

    print()
    print("VQ-19 Row Count Summary:")
    vq19_ok = True
    for table, expected in EXPECTED_COUNTS.items():
        actual = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        ok = actual == expected
        if not ok:
            vq19_ok = False
            all_ok = False
        print(f"  {'PASS' if ok else 'FAIL'}  {table}: expected={expected} actual={actual}")

    print()
    print("=" * 60)
    print(f"OVERALL: {'ALL 19 CHECKS PASSED' if all_ok else 'FAILURES DETECTED - see above'}")
    db.close()
    return all_ok


if __name__ == "__main__":
    import sys
    ok = run()
    sys.exit(0 if ok else 1)
