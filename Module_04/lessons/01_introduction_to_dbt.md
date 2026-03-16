# Introduction to dbt (data build tool)

## The Shift from ETL to ELT
Historically, data teams used complex drag-and-drop tools to perform **ETL (Extract, Transform, Load)**. The transformation happened in middle-tier proprietary servers before the data landed in the warehouse.

The modern standard is **ELT (Extract, Load, Transform)**. 
Because analytical engines like DuckDB, Snowflake, and BigQuery are so immensely powerful, we *Extract* and *Load* raw data directly into the warehouse/data lake first. Then, we execute the *Transformation* directly against the raw engine.

## Why dbt?
dbt standardizes the "T" in ELT. Instead of writing massive 1000-line stored procedures, dbt allows Data Engineers to write modular SQL `SELECT` statements. 

dbt handles:
1. **Boilerplate**: You just write the `SELECT` query. dbt wraps it in the `CREATE TABLE X AS` or `INSERT INTO` logic under the hood based on your materialization config.
2. **DAGs**: Every model uses explicitly defined `ref()` functions. dbt reads these and builds a **Directed Acyclic Graph (DAG)** to understand dependency order. If Model B depends on Model A, dbt builds Model A first.
3. **Testing**: Instead of writing separate Python assertion scripts, you define tests natively via simple `.yml` files (e.g., checking if an `id` is `unique` and `not_null`).
4. **Documentation**: dbt parses your project and can generate an interactive HTML website representing your entire company data model out of the box.

## Core Concepts
- **Models**: Simple `.sql` files containing logic.
- **Materializations**: How dbt builds the model in the database.
  - `view`: A saved SQL query. Fast to build, slower to query.
  - `table`: Physically writes the data. Slower to build, fast to query.
  - `incremental`: Only inserts rows since the last execution. Excellent for massive log tables.
- **Macros**: Reusable SQL code blocks written in Jinja (the templating language). You can write a macro that generates a complex CASE statement and reuse it across 50 models.
