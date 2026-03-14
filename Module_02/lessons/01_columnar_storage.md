# Lesson 2.1: Columnar Storage

## The Problem with CSVs
A Comma-Separated Values (CSV) file is a **row-based** storage format. It is designed to be easily readable by humans. However, it fails spectacularly at scale in Data Engineering for three reasons:
1. **No Schema parsing:** A CSV doesn't strictly know if a column is an integer or a string until the compute engine guesses it.
2. **Lack of Compression:** Text is bloated. 
3. **Full Table Scans:** If you have a 100GB CSV with 100 columns and you only want to `SELECT city FROM data`, the compute engine still has to read the entire 100GB row by row to extract that single column.

## Parquet: The SOTA Format
Apache Parquet is a **columnar** storage format. Data is stored column by column, rather than row by row.

**Why this is SOTA:**
1. **Column Pruning:** If you run `SELECT city`, Parquet allows the engine to *only* load the `city` column from the disk into memory, bypassing the other 99 columns entirely. This reduces I/O by orders of magnitude.
2. **High Compression:** Because a column contains similar data types (e.g., all dates in one column, all text in another), compression algorithms (like Snappy or ZSTD) are extremely effective, reducing file sizes by up to 80% compared to CSV.
3. **Built-in Schema:** Parquet files carry their schema (metadata) inside the file itself. 

In this module, we replace CSV generated pipelines completely with Parquet files.