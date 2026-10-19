IoT Sensor Data Processor
Python · NumPy · CSV Data Cleaning · Visualization

A small, reproducible data-processing application developed for the AASTU AWS AI/ML Cohort — Week 1 Lab. It reads synthetic temperature and humidity measurements from three sensors, validates and cleans the records, computes NumPy-based statistics, and saves CSV reports and a temperature trend chart.

Open the Google Colab notebook · [View the notebook on GitHub](notebooks/IoT_Sensor_Data_Processing.ipynb)
Overview
The workflow is:

Raw CSV → load_csv() → clean_data() → analyze_data() → CSV reports + temperature chart

The processor provides:
- CSV loading and reusable data-cleaning functions.
- Timestamp, sensor ID, numeric-value, and duplicate validation.
- Vectorized NumPy statistics and rule-based alert flags.
- Overall and per-sensor summaries.
- Exportable reports and a Matplotlib chart.
- A standalone Jupyter/Google Colab notebook and automated unit tests.
Sample results
The included dataset contains 38 synthetic readings from ROOM_A, ROOM_B, and ROOM_C, including deliberately invalid records.
Metric	Result
Raw records	38
Valid records	30
Rejected records	8
Average temperature	26.82 °C
Average humidity	61.23%
Readings flagged	14


Sensor	Valid readings	Average temperature	Flagged readings
ROOM_A	10	25.54 °C	0
ROOM_B	10	31.47 °C	7
ROOM_C	10	23.45 °C	7



Data validation and analysis
Each record contains timestamp, sensor_id, temperature_c, and humidity_pct.

The cleaning stage trims and capitalizes sensor IDs, validates timestamps and numeric fields, rejects non-finite or missing values, and removes duplicate (timestamp, sensor_id) pairs. The sample accepts temperatures between −20 °C and 60 °C and humidity between 0% and 100%.

NumPy calculates minimum, maximum, and mean values and groups readings by sensor using Boolean masks. A reading is flagged when temperature ≥ 30 °C or humidity ≥ 70%.

These thresholds are illustrative rules for a programming exercise, not engineering safety limits or predictions from a trained machine-learning model.
Run locally
Requires Python 3 and Git. From PowerShell on Windows:
git clone https://github.com/Aman21adu/iot-sensor-data-processing.git
cd iot-sensor-data-processing
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\src\processor.py
Run the automated tests:
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
The processor saves cleaned_sensor_readings.csv, sensor_summary.csv, and temperature_trend.png in outputs/. The .venv/ environment is excluded from version control.
Google Colab
Use the runnable Colab notebook, or open [`notebooks/IoT_Sensor_Data_Processing.ipynb`](notebooks/IoT_Sensor_Data_Processing.ipynb) in Jupyter. The notebook contains the loading, cleaning, analysis, and plotting functions and can run independently of src/processor.py.

In a fresh Colab session, upload [`data/raw_sensor_readings.csv`](data/raw_sensor_readings.csv) when prompted and run all cells.
Repository structure
├── data/
│   └── raw_sensor_readings.csv
├── notebooks/
│   └── IoT_Sensor_Data_Processing.ipynb
├── outputs/
│   ├── cleaned_sensor_readings.csv
│   ├── sensor_summary.csv
│   └── temperature_trend.png
├── src/
│   ├── __init__.py
│   └── processor.py
├── tests/
│   └── test_processor.py
├── .gitignore
├── requirements.txt
└── README.md
Scope
This is an educational demonstration using fabricated sensor data. It does not collect live readings, deploy a monitoring service, or train a machine-learning model.
