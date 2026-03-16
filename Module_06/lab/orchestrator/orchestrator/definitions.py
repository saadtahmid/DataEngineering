import os
from pathlib import Path
from dagster import AssetExecutionContext, Definitions, load_assets_from_modules

# Import our standard python assets
from . import assets

# In Docker, we mounted the volume to /opt/dagster/dbt_project
DBT_PROJECT_DIR = Path("/opt/dagster/dbt_project").resolve()

# We need dagster_dbt to orchestrate our previous transformations
from dagster_dbt import DbtCliResource, dbt_assets

@dbt_assets(manifest=DBT_PROJECT_DIR / "target" / "manifest.json")
def my_platform_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# Gather all SDAs (python + dbt)
all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=[*all_assets, my_platform_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(DBT_PROJECT_DIR)),
    },
)
