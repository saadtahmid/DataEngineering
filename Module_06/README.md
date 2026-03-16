# Module 5: Orchestration (Dagster)

Welcome to Module 5! We now have extraction (Polars), storage (MinIO), and transformation (dbt). But in a real environment, no pipeline runs manually via your terminal. You need an orchestrator to schedule tasks, manage retries, handle dependencies, and alert you when things fail.

For years, the industry standard was **Apache Airflow**. However, Airflow is heavily task-oriented (e.g., "Run Script A", then "Run Script B") and struggles with modern data concepts. 

We will use **Dagster**, a State-of-the-Art data orchestrator designed around **Software-Defined Assets (SDAs)**. Instead of tracking *tasks*, Dagster tracks the *data assets* those tasks produce (e.g., "table X", "ML model Y").

## Lesson Structure
- `lessons/01_introduction_to_orchestration.md`: Why do we need orchestration, and Dagster vs Airflow.
- `lessons/02_software_defined_assets.md`: The paradigm shift of focusing on data outputs rather than execution DAGs.

## Hands-On Lab Setup: The Dagster Project

In this lab, we will orchestrate the end-to-end flow: fetching our raw data, loading it (mocked/symbolic here), and triggering our dbt models from Module 4 using `dagster-dbt`. 

1. **Setup Python Environment & Install Dagster**
   ```bash
   cd lab/orchestrator
   python3 -m venv .venv
   source .venv/bin/activate
   pip install dagster dagster-webserver dagster-dbt dbt-duckdb polars
   ```

2. **Prepare the dbt Manifest**
   Dagster needs to read our dbt project's `manifest.json` to understand the dependency graph. Let's compile it in the Module 4 directory.
   ```bash
   cd ../../Module_04/lab/my_platform
   dbt parse
   cd ../../../Module_05/lab/orchestrator
   ```

3. **Start the Dagster UI**
   ```bash
   dagster dev
   ```
   *Note: Open the link provided in the terminal (usually http://localhost:3000) to view your Dagster instance.*
