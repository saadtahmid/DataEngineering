# Data Modeling Fundamentals

Now that we have the raw, untyped JSON and Parquet from Module 1 & 2 loading into MinIO (Module 3), we need to organize it. If we build complicated analytics directly on raw data, we'll hit massive problems when upstream systems (like Postgres columns) inevitably change.

To prevent cascading breakages, Data Engineering generally follows a multi-tiered architecture (often called the **Medallion Architecture**, championed by Databricks, though the concept of staging and dimensional modeling is decades old).

## The Bronze Layer (Raw)
- Also called **Source Conformed**.
- The rawest data pulled from upstream.
- **Rule**: Never modify data in Bronze. It is an exact replica of source systems (e.g., MinIO Parquet dumps, Postgres CDC tables).

## The Silver Layer (Staging)
- Your first line of defense. We use `models/staging/` to handle:
  - Renaming vague columns (`dt` -> `event_date`)
  - Casting strings to integers or timestamps
  - Deduping raw rows
  - Simple mapping (`state = 'CA'` -> `'California'`)
- **Rule**: Staging models must map 1:1 with source tables. Don't aggregate or join massive datasets here.

## The Gold Layer (Marts/Dimensions & Facts)
- Also called the **Analytics Layer** or `models/marts/`.
- This is where complex engineering happens.
- We join multiple Silver staging models together.
- We perform large aggregations (e.g., `SUM(revenue) OVER (...)`).
- Data here is structured to answer Business questions.
- **Rule**: If a BI Tool is querying your data, it should *only* be hitting the Gold mart models.

## Dimensional Modeling 101 (Kimball)
While modern data often relies on massive flattened wide tables (One Big Table / OBT) because columnar engines are fast, traditional modeling remains critical:
1. **Dimensions**: The "Who, What, Where, When". Descriptive attributes (e.g., `dim_users`, `dim_products`).
2. **Facts**: The "Action". Metrics, measurements, and numerical data tied to an event (e.g., `fct_orders`, `fct_pageviews`). Facts are usually massive and link out to Dimensions via foreign keys.
