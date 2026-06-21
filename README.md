Financial ETL & BI Dashboard
A Python-based data pipeline and interactive business intelligence dashboard simulating the processing of multi-source banking transactions.

Architecture & Data Flow
Ingestion (Extract): generate_data.py creates 3 synthetic CSVs (Online, Branch, ATM) in data/raw/, simulating different source systems with varying data quality issues.
Processing (Transform & Validate): pipeline.py extracts the raw CSVs, standardizes schemas, deduplicates records, and enforces data integrity checks (e.g., dropping null customer_ids, flagging negative amounts).
Logging: Validation failures are strictly logged to data/processed/validation_report.log rather than silently dropped.
Storage (Load): The curated dataset is saved as an optimized .parquet file in data/processed/.
Presentation: A Streamlit dashboard (app.py) reads the Parquet file and provides interactive filtering, KPI calculations, and Plotly visualizations.
How to Run
Setup Environment:
python -m venv venvsource venv/bin/activate  # On Windows: venv\Scripts\activatepip install -r requirements.txt
Generate Synthetic Data:
bash

cd etl
python generate_data.py
Run the ETL Pipeline:
bash

python pipeline.py
# Check data/processed/validation_report.log to see the cleaned dirty data!
Launch the Dashboard:
bash

cd ../dashboard
streamlit run app.py
