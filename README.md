Financial ETL & BI Dashboard
A Python-based data pipeline and interactive business intelligence dashboard simulating the processing of multi-source banking transactions.

Architecture & Data Flow
1. Ingestion (Extract): generate_data.py creates 3 synthetic CSVs (Online, Branch, ATM) in data/raw/, simulating different source systems with varying data quality issues.
2. Processing (Transform & Validate): pipeline.py extracts the raw CSVs, standardizes schemas, deduplicates records, and enforces data integrity checks (e.g., dropping null customer_ids, flagging negative amounts).
3. Logging: Validation failures are strictly logged to data/processed/validation_report.log rather than silently dropped.
4. Storage (Load): The curated dataset is saved as an optimized .parquet file in data/processed/.
5. Presentation: A Streamlit dashboard (app.py) reads the Parquet file and provides interactive filtering, KPI calculations, and Plotly visualizations.

How to Run
1. Setup Environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Generate Synthetic Data:
   ```
   cd etl
   python generate_data.py
   ```
3. Run the ETL Pipeline:
   ```
   python pipeline.py
   ```
4. Launch the Dashboard:
   ```
   cd ../dashboard
   streamlit run app.py
   ```
