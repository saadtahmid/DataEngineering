# Modern Orchestration (Dagster)

If a cron job is a simple timer loop, a **Data Orchestrator** is an intelligent central nervous system for your engineering pipelines. It handles scheduling, retries, failing gracefully, and mapping out the dependency order of your code.

## Airflow vs. Dagster
For nearly a decade, **Apache Airflow** dominated this space. It defined pipelines as DAGs (Directed Acyclic Graphs) of *Tasks*. 
- Task A (Extract) -> Task B (Transform) -> Task C (Load).
- However, Airflow doesn't know anything about the *data itself*. It only knows "Task A finished successfully." 

**Dagster** represents the modern SOTA standard. It relies on **Software-Defined Assets (SDAs)**.

## Software-Defined Assets (SDAs)
In Dagster, you define the *thing you want to exist* (an asset), and the function body is just *how* to materialize it. You use the `@asset` decorator.

```python
from dagster import asset
import polars as pl

@asset
def raw_users():
    # Returns the physical asset data!
    return pl.read_csv("https://api.example.com/users")

@asset
def fct_user_metrics(raw_users):
    # Notice we pass the upstream asset as a python argument!
    # Dagster automatically wires this as a dependency.
    return raw_users.group_by("department").agg(pl.count())
```

### Why this is SOTA
1. **Asset Lineage**: Your orchestrator UI visually displays `raw_users` connecting to `fct_user_metrics`. If a business user asks, "How is the `fct_user_metrics` table built?", they see the exact graph and code in the Dagster UI without reading GitHub.
2. **dbt Integration**: dbt is already an asset-based tool. Dagster ingests dbt projects seamlessly. Every single dbt model becomes a Dagster Software-Defined Asset automatically! You get the ultimate view of your entire ELT pipeline from extraction down to final BI tables.
