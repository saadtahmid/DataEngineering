# Lesson 1.2: Advanced SQL Thinking

## Moving Beyond SELECT *
While basic `SELECT`, `WHERE`, and `JOIN` statements are the bread and butter of database querying, a Data Engineer must think in **sets**. Modern SQL provides advanced tooling to perform complex aggregations, sequential logic, and performance tuning natively in the database engine.

## 1. Common Table Expressions (CTEs)
A CTE acts as a temporary view or table that exists only for the duration of the query. Introduced by the `WITH` clause, CTEs make deeply nested queries readable and modular.

```sql
WITH ActiveUsers AS (
    SELECT user_id, email, city 
    FROM users 
    WHERE status = 'active'
),
OrderCounts AS (
    SELECT user_id, COUNT(*) as total_orders
    FROM orders
    GROUP BY user_id
)
-- We can now cleanly join our temporary CTEs
SELECT a.email, a.city, o.total_orders
FROM ActiveUsers a
JOIN OrderCounts o ON a.user_id = o.user_id;
```
*Why this is SOTA:* CTEs heavily reduce spaghetti code. Some engines (like PostgreSQL) can also materialize CTEs intelligently, improving optimization over legacy nested subqueries.

## 2. Window Functions
Traditional `GROUP BY` aggregations collapse your rows. You lose the individual row detail in exchange for the summary. 
**Window functions** allow you to calculate aggregations "over a window" of rows related to the current row, *without* collapsing them.

```sql
SELECT 
    name,
    department,
    salary,
    -- Rank employees by salary WITHIN their specific department
    RANK() OVER(PARTITION BY department ORDER BY salary DESC) as dept_salary_rank
FROM employees;
```
Key concepts here:
*   `OVER()`: Defines the window.
*   `PARTITION BY`: Chunks the data into groups (like GROUP BY, but without collapsing).
*   `ORDER BY`: Sorts the rows within that partition.

## 3. Query Execution Plans
You wrote the SQL, but how does the database actually execute it? RDBMS engines use an Optimizer. As Data Engineers, we must verify our queries aren't scanning millions of rows unnecessarily.

Using `EXPLAIN ANALYZE <your query>` in PostgreSQL tells the engine to run the query and report back the actual execution steps (Sequential Scans, Index Scans, Hash Joins) and the time taken. 
This is the ultimate tool for debugging slow pipelines.