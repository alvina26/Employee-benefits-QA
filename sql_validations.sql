-- =============================================================
-- sql_validations.sql
-- Employee Benefits Enrollment QA Validation Project
-- Purpose : A library of documented SQL checks that can be run
--           against the benefits_enrollment.db to detect data
--           quality and business-rule violations.
-- Usage   : sqlite3 benefits_enrollment.db < sql_validations.sql
--           Or paste individual queries into any SQLite client.
-- Expected baseline result : All queries return 0 rows when run
--   against the valid baseline data loaded by setup_db.py.
--   Queries against the intentionally invalid data return the
--   number of bad rows described in each comment.
-- =============================================================

-- Enable column-name headers so results are readable.
.headers on
.mode column

-- =============================================================
-- SECTION 1 : Missing required values (NULL checks)
-- =============================================================

-- VQ-01 : Employees with NULL employee_id
-- Business rule : BR-01 — every employee must have a unique ID.
-- Expected on baseline : 0 rows.
-- Expected on invalid_employees fixture : 1 row (row with empty ID).
SELECT 'VQ-01' AS check_id,
       'NULL employee_id' AS violation,
       employee_id, first_name, last_name
FROM   employees
WHERE  employee_id IS NULL OR TRIM(employee_id) = '';

-- VQ-02 : Employees with NULL or empty hire_date
-- Business rule : BR-01 — hire_date is mandatory.
-- Expected on baseline : 0 rows.
SELECT 'VQ-02' AS check_id,
       'NULL hire_date' AS violation,
       employee_id, first_name, last_name, hire_date
FROM   employees
WHERE  hire_date IS NULL OR TRIM(hire_date) = '';

-- VQ-03 : Benefit plans with NULL plan_id
-- Business rule : BR-01 — every plan must have a unique ID.
-- Expected on baseline : 0 rows.
SELECT 'VQ-03' AS check_id,
       'NULL plan_id' AS violation,
       plan_id, plan_name
FROM   benefit_plans
WHERE  plan_id IS NULL OR TRIM(plan_id) = '';

-- VQ-04 : Enrollments with NULL enrollment_id
-- Business rule : BR-01 — every enrollment record must have an ID.
-- Expected on baseline : 0 rows.
SELECT 'VQ-04' AS check_id,
       'NULL enrollment_id' AS violation,
       enrollment_id, employee_id, plan_id
FROM   enrollments
WHERE  enrollment_id IS NULL OR TRIM(enrollment_id) = '';

-- VQ-05 : Enrollments missing employee_id, plan_id, enrollment_date,
--          coverage_start, or status
-- Business rule : BR-01 — all these fields are required.
-- Expected on baseline : 0 rows.
SELECT 'VQ-05' AS check_id,
       'Missing required enrollment field' AS violation,
       enrollment_id, employee_id, plan_id, enrollment_date,
       coverage_start, status
FROM   enrollments
WHERE  employee_id     IS NULL OR TRIM(employee_id)     = ''
   OR  plan_id         IS NULL OR TRIM(plan_id)         = ''
   OR  enrollment_date IS NULL OR TRIM(enrollment_date) = ''
   OR  coverage_start  IS NULL OR TRIM(coverage_start)  = ''
   OR  status          IS NULL OR TRIM(status)          = '';

-- =============================================================
-- SECTION 2 : Duplicate identifier checks
-- =============================================================

-- VQ-06 : Duplicate employee_id values
-- Business rule : BR-01 — employee IDs must be unique.
-- Expected on baseline : 0 rows.
SELECT 'VQ-06' AS check_id,
       'Duplicate employee_id' AS violation,
       employee_id,
       COUNT(*) AS occurrences
FROM   employees
GROUP  BY employee_id
HAVING COUNT(*) > 1;

-- VQ-07 : Duplicate plan_id values
-- Business rule : BR-01 — plan IDs must be unique.
-- Expected on baseline : 0 rows.
SELECT 'VQ-07' AS check_id,
       'Duplicate plan_id' AS violation,
       plan_id,
       COUNT(*) AS occurrences
FROM   benefit_plans
GROUP  BY plan_id
HAVING COUNT(*) > 1;

-- VQ-08 : Duplicate enrollment_id values
-- Business rule : BR-01 — enrollment IDs must be unique.
-- Expected on baseline : 0 rows.
SELECT 'VQ-08' AS check_id,
       'Duplicate enrollment_id' AS violation,
       enrollment_id,
       COUNT(*) AS occurrences
FROM   enrollments
GROUP  BY enrollment_id
HAVING COUNT(*) > 1;

-- VQ-09 : Duplicate APPROVED enrollments (same employee + plan)
-- Business rule : BR-08 — an employee may not hold two APPROVED
--                enrollments for the same plan simultaneously.
-- Expected on baseline : 0 rows.
SELECT 'VQ-09' AS check_id,
       'Duplicate APPROVED enrollment for same employee+plan' AS violation,
       employee_id,
       plan_id,
       COUNT(*) AS approved_count
FROM   enrollments
WHERE  status = 'APPROVED'
GROUP  BY employee_id, plan_id
HAVING COUNT(*) > 1;

-- =============================================================
-- SECTION 3 : Orphaned foreign-key references
-- =============================================================

-- VQ-10 : Enrollments referencing non-existent employees
-- Business rule : BR-02 — enrollment must link to a real employee.
-- Expected on baseline : 0 rows.
SELECT 'VQ-10' AS check_id,
       'Enrollment references non-existent employee' AS violation,
       e.enrollment_id,
       e.employee_id
FROM   enrollments e
WHERE  NOT EXISTS (
    SELECT 1 FROM employees emp WHERE emp.employee_id = e.employee_id
);

-- VQ-11 : Enrollments referencing non-existent plans
-- Business rule : BR-03 — enrollment must link to a real plan.
-- Expected on baseline : 0 rows.
SELECT 'VQ-11' AS check_id,
       'Enrollment references non-existent plan' AS violation,
       e.enrollment_id,
       e.plan_id
FROM   enrollments e
WHERE  NOT EXISTS (
    SELECT 1 FROM benefit_plans p WHERE p.plan_id = e.plan_id
);

-- VQ-12 : Dependents referencing non-existent employees
-- Business rule : BR-10 — dependent must link to a real employee.
-- Expected on baseline : 0 rows.
SELECT 'VQ-12' AS check_id,
       'Dependent references non-existent employee' AS violation,
       d.dependent_id,
       d.employee_id
FROM   dependents d
WHERE  NOT EXISTS (
    SELECT 1 FROM employees emp WHERE emp.employee_id = d.employee_id
);

-- =============================================================
-- SECTION 4 : Enrollment eligibility inconsistencies
-- =============================================================

-- VQ-13 : APPROVED enrollments for INACTIVE or TERMINATED employees
-- Business rule : BR-04 — only ACTIVE employees may have APPROVED
--                enrollments.
-- Expected on baseline : 0 rows.
SELECT 'VQ-13' AS check_id,
       'APPROVED enrollment for non-ACTIVE employee' AS violation,
       e.enrollment_id,
       emp.employee_id,
       emp.employment_status,
       e.status AS enrollment_status
FROM   enrollments e
JOIN   employees   emp ON emp.employee_id = e.employee_id
WHERE  e.status = 'APPROVED'
  AND  emp.employment_status <> 'ACTIVE';

-- VQ-14 : APPROVED enrollments for ineligible employees (eligible = 0)
-- Business rule : BR-04 — ineligible employees must not receive
--                APPROVED enrollments.
-- Expected on baseline : 0 rows.
-- NOTE : EMP012 in the baseline has eligible=0 but no APPROVED enrollment;
--        the invalid fixture tests ENR_BAD9 for this violation.
SELECT 'VQ-14' AS check_id,
       'APPROVED enrollment for ineligible employee' AS violation,
       e.enrollment_id,
       emp.employee_id,
       emp.eligible,
       e.status AS enrollment_status
FROM   enrollments e
JOIN   employees   emp ON emp.employee_id = e.employee_id
WHERE  e.status   = 'APPROVED'
  AND  emp.eligible = 0;

-- =============================================================
-- SECTION 5 : Invalid date ranges
-- =============================================================

-- VQ-15 : Plans where end_date is not after effective_date
-- Business rule : BR-05 — plan end_date must be strictly after
--                effective_date when end_date is present.
-- Expected on baseline : 0 rows.
SELECT 'VQ-15' AS check_id,
       'Plan end_date is not after effective_date' AS violation,
       plan_id,
       plan_name,
       effective_date,
       end_date
FROM   benefit_plans
WHERE  end_date IS NOT NULL
  AND  end_date <= effective_date;

-- VQ-16 : Enrollments where enrollment_date is before the employee's
--          hire_date
-- Business rule : BR-06 — an employee cannot enroll before being hired.
-- Expected on baseline : 0 rows.
SELECT 'VQ-16' AS check_id,
       'Enrollment date before employee hire date' AS violation,
       e.enrollment_id,
       e.employee_id,
       emp.hire_date,
       e.enrollment_date
FROM   enrollments e
JOIN   employees   emp ON emp.employee_id = e.employee_id
WHERE  e.enrollment_date < emp.hire_date;

-- VQ-17 : Enrollments where coverage_start is before enrollment_date
-- Business rule : BR-07 — coverage cannot start before the enrollment
--                date.
-- Expected on baseline : 0 rows.
SELECT 'VQ-17' AS check_id,
       'Coverage start before enrollment date' AS violation,
       enrollment_id,
       employee_id,
       enrollment_date,
       coverage_start
FROM   enrollments
WHERE  coverage_start < enrollment_date;

-- =============================================================
-- SECTION 6 : Invalid status values
-- =============================================================

-- VQ-18 : Enrollments with a status value outside the allowed set
-- Business rule : BR-09 — status must be APPROVED, PENDING, or
--                CANCELLED.
-- Expected on baseline : 0 rows.
-- Note : SQLite CHECK constraints prevent this in the main table;
--        this query is useful when validating data imported from
--        external sources before insert.
SELECT 'VQ-18' AS check_id,
       'Invalid enrollment status' AS violation,
       enrollment_id,
       employee_id,
       status
FROM   enrollments
WHERE  status NOT IN ('APPROVED', 'PENDING', 'CANCELLED');

-- =============================================================
-- SECTION 7 : Informational summary (always run last)
-- =============================================================

-- VQ-19 : Row-count summary — useful as a smoke test after loading.
-- No violation semantics; just a counts overview.
SELECT 'VQ-19' AS check_id,
       'Row counts summary (informational)' AS note,
       (SELECT COUNT(*) FROM employees)     AS employees,
       (SELECT COUNT(*) FROM benefit_plans) AS benefit_plans,
       (SELECT COUNT(*) FROM dependents)    AS dependents,
       (SELECT COUNT(*) FROM enrollments)   AS enrollments;
