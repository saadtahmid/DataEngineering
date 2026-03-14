# Lesson 2.2: State-of-the-Art DataFrames (Polars)

For years, the gold standard for data manipulation in Python was **Pandas**. However, Pandas was created before multi-core processors were standard, and it relies heavily on single-threaded, memory-intensive operations.

If you try to process a 10GB dataset with Pandas on a machine with 16GB of RAM, your program will crash with an `Out of Memory` (OOM) error.

## Enter Polars

Polars is a lightning-fast DataFrame library written in **Rust**.

**Why Polars is SOTA:**
1. **Multi-threading:** Polars automatically uses all available CPU cores. If you have an 8-core CPU, filtering a dataframe in Polars can be up to 8-10x faster out of the box.
2. **Apache Arrow Memory Model:** Polars uses Arrow, an in-memory columnar format. It avoids making expensive "deep copies" of data when transforming it.
3. **Lazy Evaluation & Query Optimizer:** 
   * In traditional tools (eager evaluation), every line of code executes sequentially.
   * In Polars (lazy evaluation), when you chain operations (`df.filter().select().groupby()`), Polars doesn't do anything yet. It builds a query plan, optimizes it (e.g., pushing the filter to the very beginning so less data is passed to the groupby), and only executes when you call `.collect()`.

## Core Syntax Differences
Unlike Pandas which relies on `df[df['col'] > 5]`, Polars uses an expressive API via `.select()` and `with_columns()`.

```python
import polars as pl

# LAZY execution: scan_parquet instead of read_parquet
q = (
    pl.scan_parquet("data.parquet")
    .filter(pl.col("age") > 30)
    .select(["name", "city"])
)

# Execution happens here
df = q.collect() 
```