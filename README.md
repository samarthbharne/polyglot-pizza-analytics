# Hybrid Polyglot Analytics Engine: NoSQL to SQL ETL Pipeline

## 📌 Overview
This project demonstrates a modern data architecture designed to handle high-velocity web clickstream data. It utilizes a **Polyglot Persistence** approach:
* **MongoDB (NoSQL):** Captures raw, unstructured user interaction logs (clicks, views, etc.).
* **PostgreSQL (SQL):** Stores structured business intelligence and customer metrics for reporting.

## 🛠️ Technical Tech Stack
* **Languages:** Python (Pandas, Pymongo, Psycopg2)
* **Databases:** MongoDB (NoSQL), PostgreSQL (Relational)
* **Tools:** pgAdmin 4, MongoDB Compass

## 🚀 The Pipeline (ETL Process)
1. **Extract:** Python pulls 5,000+ raw JSON documents from MongoDB.
2. **Transform:** Using **Pandas**, raw logs are aggregated to calculate:
   - Total user engagement (clicks).
   - Product Affinity (Favorite pizza based on view frequency).
   - Recency (Last active timestamp).
3. **Load:** Insights are "Upserted" into PostgreSQL tables using an ACID-compliant connection.


## 🧠 Technical Challenges & Solutions

### 1. Schema Impedance Mismatch
**Challenge:** MongoDB data is unstructured and flexible, while PostgreSQL requires a strict schema.
**Solution:** Implemented a transformation layer using Python's **Pandas** library to "flatten" the JSON documents and enforce data types (e.g., converting ISO timestamps to SQL-compatible DateTime objects) before loading.

### 2. Idempotency & Data Duplication
**Challenge:** Running the ETL script multiple times would create duplicate entries for Alice and Bob in the PostgreSQL metrics table.
**Solution:** Developed an **"Upsert" logic** using the `ON CONFLICT` clause in SQL. This ensures that if a record for a specific user already exists, it is updated with the latest metrics instead of creating a duplicate.

### 3. Distributed Data Integrity
**Challenge:** Ensuring that a `user_id` in a NoSQL log actually corresponds to a `customer_id` in the Relational DB.
**Solution:** Integrated a validation step in the Python script to filter out "orphaned" logs that do not match existing customer records, ensuring 100% relational integrity.

## 📊 Key Results
By bridging the gap between raw logs and structured data, the system identifies:
* **User Engagement:** Quantified activity for specific customers (e.g., Alice Smith: 2500+ interactions).
* **Targeted Insights:** Automated identification of favorite products (e.g., "Hawaiian" vs "Pepperoni") to drive marketing campaigns.
