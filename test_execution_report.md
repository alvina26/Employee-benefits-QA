# Test Execution Report
## Employee Benefits Enrollment — QA Validation

---

### Execution Details

| Field | Value |
|-------|-------|
| **Date** | 2026-10-12 |
| **Time** | 20:31 UTC+5:30 |
| **Command** | `pytest tests/ -v` |
| **Python version** | 3.12.4 |
| **pytest version** | 9.1.1 |
| **pluggy version** | 1.6.0 |
| **Platform** | win32 (Windows 10, x64) |
| **Working directory** | `employee-benefits-qa/` |
| **Database initialised by** | `python setup_db.py` (41 rows loaded across 4 tables) |

---

### Test Totals

| Metric | Count |
|--------|-------|
| **Total collected** | 63 |
| **Passed** | 63 |
| **Failed** | 0 |
| **Errors** | 0 |
| **Skipped** | 0 |
| **Duration** | 10.75 s |

**Result: ALL 63 TESTS PASSED — no failures, no errors**

---

### Results by Test File

| File | Tests | Passed | Failed | Coverage |
|------|-------|--------|--------|----------|
| `tests/test_constraints.py` | 11 | 11 | 0 | FK integrity, DELETE blocking, dependent constraints |
| `tests/test_employees.py` | 9 | 9 | 0 | Employee PK/CHECK constraints, baseline smoke tests |
| `tests/test_enrollment.py` | 14 | 14 | 0 | Enrollment business rules BR-02 through BR-09 |
| `tests/test_plans.py` | 10 | 10 | 0 | Plan validation, BR-05 date constraint |
| `tests/test_sql_validations.py` | 19 | 19 | 0 | All 19 VQ SQL checks against clean baseline data |

---

### Individual Test Results

| # | Test ID | Test Function | Result |
|---|---------|---------------|--------|
| 1 | TC-C01 | `test_constraints.py::test_valid_dependent_inserted` | PASSED |
| 2 | TC-C02 | `test_constraints.py::test_dependent_ghost_employee_rejected` | PASSED |
| 3 | TC-C03 | `test_constraints.py::test_delete_employee_with_dependents_blocked` | PASSED |
| 4 | TC-C04 | `test_constraints.py::test_delete_employee_with_enrollments_blocked` | PASSED |
| 5 | TC-C05 | `test_constraints.py::test_valid_enrollment_fk` | PASSED |
| 6 | TC-C06 | `test_constraints.py::test_invalid_dependent_relationship_rejected` | PASSED |
| 7 | TC-C07 | `test_constraints.py::test_null_dependent_id_rejected` | PASSED |
| 8 | TC-C08 | `test_constraints.py::test_duplicate_dependent_id_rejected` | PASSED |
| 9 | TC-C09 | `test_constraints.py::test_baseline_dependent_fk_valid` | PASSED |
| 10 | TC-C10 | `test_constraints.py::test_baseline_enrollment_employee_fk_valid` | PASSED |
| 11 | TC-C11 | `test_constraints.py::test_baseline_enrollment_plan_fk_valid` | PASSED |
| 12 | TC-EMP01 | `test_employees.py::test_valid_employee_inserted` | PASSED |
| 13 | TC-EMP02 | `test_employees.py::test_null_employee_id_rejected` | PASSED |
| 14 | TC-EMP03 | `test_employees.py::test_duplicate_employee_id_rejected` | PASSED |
| 15 | TC-EMP04 | `test_employees.py::test_invalid_employment_status_rejected` | PASSED |
| 16 | TC-EMP05 | `test_employees.py::test_null_hire_date_rejected` | PASSED |
| 17 | TC-EMP06 | `test_employees.py::test_invalid_eligible_value_rejected` | PASSED |
| 18 | TC-EMP07 | `test_employees.py::test_inactive_employee_stored` | PASSED |
| 19 | TC-EMP08 | `test_employees.py::test_baseline_employee_count` | PASSED |
| 20 | TC-EMP09 | `test_employees.py::test_baseline_employment_status_valid` | PASSED |
| 21 | TC-E01 | `test_enrollment.py::test_valid_enrollment_inserted` | PASSED |
| 22 | TC-E02 | `test_enrollment.py::test_null_enrollment_id_rejected` | PASSED |
| 23 | TC-E03 | `test_enrollment.py::test_duplicate_approved_enrollment_detected` | PASSED |
| 24 | TC-E04 | `test_enrollment.py::test_nonexistent_employee_rejected` | PASSED |
| 25 | TC-E05 | `test_enrollment.py::test_nonexistent_plan_rejected` | PASSED |
| 26 | TC-E06 | `test_enrollment.py::test_inactive_employee_approved_enrollment_detected` | PASSED |
| 27 | TC-E07 | `test_enrollment.py::test_terminated_employee_approved_enrollment_detected` | PASSED |
| 28 | TC-E08 | `test_enrollment.py::test_coverage_before_enrollment_detected` | PASSED |
| 29 | TC-E09 | `test_enrollment.py::test_enrollment_before_hire_detected` | PASSED |
| 30 | TC-E10 | `test_enrollment.py::test_invalid_status_rejected` | PASSED |
| 31 | TC-E11 | `test_enrollment.py::test_ineligible_employee_approved_enrollment_detected` | PASSED |
| 32 | TC-E12 | `test_enrollment.py::test_pending_enrollment_allowed` | PASSED |
| 33 | TC-E13 | `test_enrollment.py::test_cancelled_enrollment_allowed` | PASSED |
| 34 | TC-E14 | `test_enrollment.py::test_second_approved_enrollment_different_plan_allowed` | PASSED |
| 35 | TC-P01 | `test_plans.py::test_valid_plan_inserted` | PASSED |
| 36 | TC-P02 | `test_plans.py::test_null_plan_id_rejected` | PASSED |
| 37 | TC-P03 | `test_plans.py::test_duplicate_plan_id_rejected` | PASSED |
| 38 | TC-P04 | `test_plans.py::test_invalid_plan_type_rejected` | PASSED |
| 39 | TC-P05 | `test_plans.py::test_end_date_before_effective_date_rejected` | PASSED |
| 40 | TC-P06 | `test_plans.py::test_end_date_equal_effective_date_rejected` | PASSED |
| 41 | TC-P07 | `test_plans.py::test_null_end_date_allowed` | PASSED |
| 42 | TC-P08 | `test_plans.py::test_baseline_plan_count` | PASSED |
| 43 | TC-P09 | `test_plans.py::test_baseline_plan_type_valid` | PASSED |
| 44 | TC-P10 | `test_plans.py::test_valid_end_date_accepted` | PASSED |
| 45 | TC-SV01 | `test_sql_validations.py::test_vq01_no_null_employee_id` | PASSED |
| 46 | TC-SV02 | `test_sql_validations.py::test_vq02_no_null_hire_date` | PASSED |
| 47 | TC-SV03 | `test_sql_validations.py::test_vq03_no_null_plan_id` | PASSED |
| 48 | TC-SV04 | `test_sql_validations.py::test_vq04_no_null_enrollment_id` | PASSED |
| 49 | TC-SV05 | `test_sql_validations.py::test_vq05_no_missing_required_enrollment_fields` | PASSED |
| 50 | TC-SV06 | `test_sql_validations.py::test_vq06_no_duplicate_employee_id` | PASSED |
| 51 | TC-SV07 | `test_sql_validations.py::test_vq07_no_duplicate_plan_id` | PASSED |
| 52 | TC-SV08 | `test_sql_validations.py::test_vq08_no_duplicate_enrollment_id` | PASSED |
| 53 | TC-SV09 | `test_sql_validations.py::test_vq09_no_duplicate_approved_enrollment` | PASSED |
| 54 | TC-SV10 | `test_sql_validations.py::test_vq10_no_orphaned_enrollment_employee` | PASSED |
| 55 | TC-SV11 | `test_sql_validations.py::test_vq11_no_orphaned_enrollment_plan` | PASSED |
| 56 | TC-SV12 | `test_sql_validations.py::test_vq12_no_orphaned_dependent` | PASSED |
| 57 | TC-SV13 | `test_sql_validations.py::test_vq13_no_approved_enrollment_for_nonactive_employee` | PASSED |
| 58 | TC-SV14 | `test_sql_validations.py::test_vq14_no_approved_enrollment_for_ineligible_employee` | PASSED |
| 59 | TC-SV15 | `test_sql_validations.py::test_vq15_no_plan_with_invalid_date_range` | PASSED |
| 60 | TC-SV16 | `test_sql_validations.py::test_vq16_no_enrollment_before_hire_date` | PASSED |
| 61 | TC-SV17 | `test_sql_validations.py::test_vq17_no_coverage_before_enrollment` | PASSED |
| 62 | TC-SV18 | `test_sql_validations.py::test_vq18_no_invalid_status` | PASSED |
| 63 | TC-SV19 | `test_sql_validations.py::test_vq19_row_count_summary` | PASSED |

---

### SQL Validation Results (run_sql_checks.py against benefits_enrollment.db)

Executed: `python run_sql_checks.py` — same session as pytest run above.

| Check | Description | Result |
|-------|-------------|--------|
| VQ-01 | NULL employee_id | PASS (0 rows) |
| VQ-02 | NULL hire_date | PASS (0 rows) |
| VQ-03 | NULL plan_id | PASS (0 rows) |
| VQ-04 | NULL enrollment_id | PASS (0 rows) |
| VQ-05 | Missing required enrollment fields | PASS (0 rows) |
| VQ-06 | Duplicate employee_id | PASS (0 rows) |
| VQ-07 | Duplicate plan_id | PASS (0 rows) |
| VQ-08 | Duplicate enrollment_id | PASS (0 rows) |
| VQ-09 | Duplicate APPROVED same employee+plan | PASS (0 rows) |
| VQ-10 | Orphaned enrollment → employee | PASS (0 rows) |
| VQ-11 | Orphaned enrollment → plan | PASS (0 rows) |
| VQ-12 | Orphaned dependent → employee | PASS (0 rows) |
| VQ-13 | APPROVED enrollment for non-ACTIVE employee | PASS (0 rows) |
| VQ-14 | APPROVED enrollment for ineligible employee | PASS (0 rows) |
| VQ-15 | Plan end_date <= effective_date | PASS (0 rows) |
| VQ-16 | Enrollment date before hire date | PASS (0 rows) |
| VQ-17 | Coverage start before enrollment date | PASS (0 rows) |
| VQ-18 | Invalid enrollment status | PASS (0 rows) |
| VQ-19 | Row count summary: employees=12, plans=8, dependents=7, enrollments=14 | PASS |

---

### Negative Fixture Verification (verify_negative_fixtures.py)

Executed: `python verify_negative_fixtures.py` — confirmed all 18 invalid scenarios
are detected by the stated constraint or SQL check.

| Fixture | Scenario | Detection Method | Result |
|---------|----------|-----------------|--------|
| invalid_employees | NULL employee_id | PRIMARY KEY NOT NULL | PASS |
| invalid_employees | Duplicate employee_id | PRIMARY KEY UNIQUE | PASS |
| invalid_employees | Invalid employment_status | CHECK constraint | PASS |
| invalid_employees | NULL hire_date | NOT NULL constraint | PASS |
| invalid_employees | eligible=2 | CHECK (eligible IN (0,1)) | PASS |
| invalid_plans | NULL plan_type | NOT NULL constraint | PASS |
| invalid_plans | end_date < effective_date | CHECK (BR-05) | PASS |
| invalid_plans | end_date = effective_date | CHECK (BR-05) | PASS |
| invalid_plans | NULL plan_id | PRIMARY KEY NOT NULL | PASS |
| invalid_enrollments | Non-existent employee_id | FOREIGN KEY (BR-02) | PASS |
| invalid_enrollments | Non-existent plan_id | FOREIGN KEY (BR-03) | PASS |
| invalid_enrollments | INACTIVE employee APPROVED | VQ-13 SQL check (BR-04) | PASS |
| invalid_enrollments | TERMINATED employee APPROVED | VQ-13 SQL check (BR-04) | PASS |
| invalid_enrollments | Duplicate APPROVED same emp+plan | VQ-09 SQL check (BR-08) | PASS |
| invalid_enrollments | coverage_start before enrollment_date | VQ-17 SQL check (BR-07) | PASS |
| invalid_enrollments | enrollment_date before hire_date | VQ-16 SQL check (BR-06) | PASS |
| invalid_enrollments | Invalid status 'DRAFTED' | CHECK (BR-09) | PASS |
| invalid_enrollments | Ineligible employee (eligible=0) APPROVED | VQ-14 SQL check (BR-04) | PASS |

---

### Test Quality Notes

All 63 tests were reviewed for assertion quality. They do not merely assert that
no exception was raised (except where the expected outcome IS an exception, e.g.
TC-E02). Specifically:

- **Positive tests** (e.g. TC-E01) assert that stored field values match the
  inserted values, not just that the INSERT succeeded.
- **Negative tests detecting violations via SQL** (e.g. TC-E06, TC-E08) insert the
  bad row, then run the equivalent VQ query and assert the specific enrollment_id
  appears in the results — verifying detection, not just row existence.
- **Negative tests expecting exceptions** (e.g. TC-E04, TC-E10) use `pytest.raises`
  specifically for `sqlite3.IntegrityError`, meaning any other exception would fail
  the test.
- **Baseline smoke tests** (e.g. TC-EMP08, TC-SV19) assert exact expected counts,
  so any accidental mutation of the baseline CSV files would be caught.

---

### Setup Verification

`python setup_db.py` output (fresh run before tests):

```
Initialising database: benefits_enrollment.db
Schema file          : schema.sql

Applying schema ...
  [OK] Schema applied from schema.sql

Loading baseline data ...
  [OK] Loaded  12 row(s) from employees.csv -> employees
  [OK] Loaded   8 row(s) from benefit_plans.csv -> benefit_plans
  [OK] Loaded   7 row(s) from dependents.csv -> dependents
  [OK] Loaded  14 row(s) from enrollments.csv -> enrollments

Done. 41 total row(s) loaded into benefits_enrollment.db.

Row counts after initialisation:
  Table                 Rows
  ---------------------------
  employees               12
  benefit_plans            8
  dependents              7
  enrollments             14
```

---

### Issues Encountered and Resolved

| Issue | Root Cause | Resolution |
|-------|-----------|------------|
| `UnicodeEncodeError` in `setup_db.py` on first run | Windows cp1252 console cannot encode U+2192 (→) in a print statement | Replaced `→` with ASCII `->` in the print string (cosmetic display only — no logic change) |

---

### Known Limitations

1. **BR-04 and BR-08 are not enforced at DB INSERT level.** SQLite CHECK constraints
   cannot span rows or join tables. These rules are validated by SQL queries
   (VQ-09, VQ-13, VQ-14) and the corresponding pytest tests. See `defect_log.csv`
   for the design notes.

2. **Dates stored as TEXT (ISO-8601).** SQLite has no native DATE type. The format
   `YYYY-MM-DD` enables correct lexicographic comparison for all date checks used here.

3. **No test for concurrent access.** This is a single-user educational project.

4. **`benefits_enrollment.db` is not committed to git** and must be regenerated
   after cloning with `python setup_db.py`.
