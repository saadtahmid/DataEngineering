# Lesson 1.1: Relational Data & PostgreSQL

## The Relational Paradigm
Before we dive into big data, data lakes, and complex distributed systems, we must understand the foundation of modern data storage: the Relational Database Management System (RDBMS). PostgreSQL is the industry-standard, state-of-the-art open-source RDBMS.

Unlike unstructured data or NoSQL document stores (like MongoDB), relational databases enforce strict structure, data integrity, and relationships between entities.

## 1. Database Normalization
Normalization is the process of organizing data to reduce redundancy and improve data integrity. While Data Engineers often *denormalize* data later in the pipeline for analytical read performance (OLAP), transactional systems (OLTP) rely heavily on normalization.

*   **First Normal Form (1NF):** Eliminate repeating groups. Every column must hold atomic (indivisible) values.
*   **Second Normal Form (2NF):** Must be in 1NF, and all non-key attributes must depend fully on the primary key.
*   **Third Normal Form (3NF):** Must be in 2NF, and there should be no transitive dependencies (non-key columns shouldn't depend on other non-key columns).

## 2. Primary and Foreign Keys
Keys are how we build relations (the "R" in RDBMS) between normalized tables.

*   **Primary Key (PK):** A unique identifier for a row in a table. It cannot be null. (e.g., `user_id SERIAL PRIMARY KEY`).
*   **Foreign Key (FK):** A column (or set of columns) in one table that references the Primary Key in another table. It enforces referential integrity so you cannot insert a record with an invalid reference.

## 3. Standard Data Types
PostgreSQL is strongly typed. Choosing the right data type is crucial for performance and storage efficiency.

*   **Numeric:** `INT`, `BIGINT`, `DECIMAL(precision, scale)`
*   **Character/Text:** `VARCHAR(n)` (variable length with limit), `TEXT` (unlimited length).
*   **Temporal:** `TIMESTAMP` (no timezone), `TIMESTAMPTZ` (with timezone), `DATE`.
*   **Advanced:** PostgreSQL also supports SOTA modern types like `JSONB` for semi-structured data, and vector embeddings (`pgvector`), bridging the gap between traditional RDBMS and specialized systems.

*Next, we will look at how to query this data using advanced SQL concepts!*
