-- =============================================================
-- schema.sql
-- Employee Benefits Enrollment QA Validation Project
-- Purpose : Define the SQLite database schema used by the
--           simulated benefits enrollment system.
-- Note    : All data is fictional and for educational purposes.
-- =============================================================

-- Drop tables in reverse dependency order so the script is
-- safe to run multiple times during development and testing.
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS dependents;
DROP TABLE IF EXISTS benefit_plans;
DROP TABLE IF EXISTS employees;

-- -------------------------------------------------------------
-- EMPLOYEES
-- Stores fictional employee records.
-- employment_status : ACTIVE | INACTIVE | TERMINATED
-- eligible          : 1 (true) if the employee meets the
--                     eligibility criteria defined in the
--                     fictional business rules; 0 otherwise.
-- -------------------------------------------------------------
CREATE TABLE employees (
    employee_id       TEXT    NOT NULL,
    first_name        TEXT    NOT NULL,
    last_name         TEXT    NOT NULL,
    employment_status TEXT    NOT NULL CHECK (employment_status IN ('ACTIVE','INACTIVE','TERMINATED')),
    hire_date         TEXT    NOT NULL,   -- ISO-8601 YYYY-MM-DD
    eligible          INTEGER NOT NULL DEFAULT 1 CHECK (eligible IN (0, 1)),
    department        TEXT,
    CONSTRAINT pk_employees PRIMARY KEY (employee_id)
);

-- -------------------------------------------------------------
-- BENEFIT PLANS
-- Stores fictional benefit plan definitions.
-- plan_type    : MEDICAL | DENTAL | VISION | LIFE
-- end_date     : NULL means the plan is still open-ended.
-- -------------------------------------------------------------
CREATE TABLE benefit_plans (
    plan_id        TEXT NOT NULL,
    plan_name      TEXT NOT NULL,
    plan_type      TEXT NOT NULL CHECK (plan_type IN ('MEDICAL','DENTAL','VISION','LIFE')),
    effective_date TEXT NOT NULL,   -- ISO-8601 YYYY-MM-DD
    end_date       TEXT,            -- ISO-8601 YYYY-MM-DD or NULL
    description    TEXT,
    CONSTRAINT pk_benefit_plans PRIMARY KEY (plan_id),
    -- BR-05: effective_date must precede end_date when end_date is present.
    CONSTRAINT chk_plan_dates CHECK (end_date IS NULL OR end_date > effective_date)
);

-- -------------------------------------------------------------
-- DEPENDENTS  (optional extension)
-- Links a fictional dependent to an employee.
-- relationship : SPOUSE | CHILD | DOMESTIC_PARTNER
-- -------------------------------------------------------------
CREATE TABLE dependents (
    dependent_id  TEXT NOT NULL,
    employee_id   TEXT NOT NULL,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,   -- ISO-8601 YYYY-MM-DD
    relationship  TEXT NOT NULL CHECK (relationship IN ('SPOUSE','CHILD','DOMESTIC_PARTNER')),
    CONSTRAINT pk_dependents PRIMARY KEY (dependent_id),
    -- BR-10: dependent must reference a real employee.
    CONSTRAINT fk_dependents_employee
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);

-- -------------------------------------------------------------
-- ENROLLMENTS
-- Records which employee enrolled in which plan.
-- status : APPROVED | PENDING | CANCELLED
-- -------------------------------------------------------------
CREATE TABLE enrollments (
    enrollment_id    TEXT NOT NULL,
    employee_id      TEXT NOT NULL,
    plan_id          TEXT NOT NULL,
    enrollment_date  TEXT NOT NULL,   -- ISO-8601 YYYY-MM-DD
    coverage_start   TEXT NOT NULL,   -- ISO-8601 YYYY-MM-DD
    status           TEXT NOT NULL CHECK (status IN ('APPROVED','PENDING','CANCELLED')),
    notes            TEXT,
    CONSTRAINT pk_enrollments PRIMARY KEY (enrollment_id),
    -- BR-02: enrollment must reference a real employee.
    CONSTRAINT fk_enrollment_employee
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    -- BR-03: enrollment must reference a real plan.
    CONSTRAINT fk_enrollment_plan
        FOREIGN KEY (plan_id)     REFERENCES benefit_plans (plan_id)
);

-- -------------------------------------------------------------
-- INDEX: speed up common QA look-ups
-- -------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_enrollments_employee ON enrollments (employee_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_plan     ON enrollments (plan_id);
CREATE INDEX IF NOT EXISTS idx_dependents_employee  ON dependents  (employee_id);
