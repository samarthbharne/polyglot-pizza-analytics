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



## 📊 Key Results
By bridging the gap between raw logs and structured data, the system identifies:
* **User Engagement:** Quantified activity for specific customers (e.g., Alice Smith: 2500+ interactions).
* **Targeted Insights:** Automated identification of favorite products (e.g., "Hawaiian" vs "Pepperoni") to drive marketing campaigns.