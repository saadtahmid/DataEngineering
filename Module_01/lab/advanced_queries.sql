-- =========================================================================
-- Hands-On Lab 1: Advanced SQL Analytics (PostgreSQL)
-- =========================================================================
-- Before running these queries, ensure you have executed:
-- `python3 lessons/03_ingest_api_to_postgres.py` to load the mock data.

-- -------------------------------------------------------------------------
-- Query 1: Basic Verification
-- Check if the Python script successfully inserted the users into our table.
-- -------------------------------------------------------------------------
SELECT 
    id, 
    name, 
    email, 
    city,
    company_name
FROM users 
ORDER BY id ASC;


-- -------------------------------------------------------------------------
-- Query 2: Common Table Expressions (CTEs)
-- CTEs make complex, nested logic much easier to read by breaking it down 
-- into sequential, temporary views.
-- Goal: Find all users who live in a city starting with the letter 'A' or 'M'
-- -------------------------------------------------------------------------
WITH TargetCities AS (
    SELECT DISTINCT city
    FROM users
    WHERE city LIKE 'A%' OR city LIKE 'M%'
)
SELECT 
    u.name,
    u.company_name,
    t.city
FROM users u
INNER JOIN TargetCities t ON u.city = t.city;


-- -------------------------------------------------------------------------
-- Query 3: Window Functions (ROW_NUMBER & RANK)
-- Window functions allow us to look at "windows" of rows around the current
-- row, WITHOUT losing the individual row data (unlike a GROUP BY).
-- Goal: Assign a pseudo-rank to users partitioned by the length of their company name.
-- -------------------------------------------------------------------------
WITH CompanyNameLengths AS (
    SELECT 
        name,
        company_name,
        LENGTH(company_name) as comp_len
    FROM users
)
SELECT 
    name,
    company_name,
    comp_len,
    -- RANK() assigns ranking based on the alphabetical order of user names 
    -- WITHIN each specific company name length grouping
    RANK() OVER (PARTITION BY comp_len ORDER BY name ASC) as student_rank
FROM CompanyNameLengths;
