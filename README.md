# IoT Sensor Data Processor — Python + NumPy

**AASTU AWS AI/ML Cohort, Week 1 Lab:** A small, reproducible Python data-processing app.

This project loads a **synthetic** IoT sensor CSV, cleans incorrect readings with reusable Python functions, analyzes temperature and humidity using **NumPy**, and exports reports and a chart. It is a learning demo, **not** a deployed IoT monitoring or ML system.

## Assignment checklist

| Requirement | Where it is demonstrated |
| --- | --- |
| Load raw CSV dataset | `data/raw_sensor_readings.csv`, `load_csv()` |
| Clean data with functions | `clean_data()` in script and notebook |
| Process with NumPy | `analyze_data()`: NumPy arrays, `mean`, `min`, `max`, boolean masks |
| Run in Google Colab / Jupyter | `notebooks/IoT_Sensor_Data_Processing.ipynb` |
| Use virtual environment | `python -m venv .venv` instructions below |
| Provide requirements.txt | `requirements.txt` |
| GitHub repo and clear README | This README; add notebook and script to your repository |

## Dataset and cleaning rules

The CSV represents three demonstration sensors (**ROOM_A**, **ROOM_B**, **ROOM_C**) over ten timestamps each, plus deliberately corrupted records. It contains 38 raw rows:

- Trim spaces and standardize sensor IDs to uppercase.
- Check timestamps and numeric measurements.
- Reject empty/malformed/non-finite values.
- Reject measurements outside demo limits of **−20 to 60 °C** or **0 to 100% humidity**.
- Remove repeated `(sensor_id, timestamp)` pairs, keeping the first valid reading.
- Flag temperature **≥30 °C** or humidity **≥70%** using vectorized NumPy comparisons. **These are demonstration thresholds, not safety or engineering standards.**

**Expected output:** 30 clean readings, 8 rejected, 14 flagged readings. The full results are exported to `outputs/`.

## Project structure

```text
IoT_Sensor_Data_Processing/
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
```

## Option A — Google Colab (easiest)

1. Open [Google Colab](https://colab.research.google.com/).
2. Choose **File → Upload notebook** and select `notebooks/IoT_Sensor_Data_Processing.ipynb`.
3. Select **Runtime → Run all**. If asked, upload `data/raw_sensor_readings.csv` from the project ZIP. If the notebook has access to the whole repository, it will detect the CSV automatically.
4. Read the cleaning summary, the NumPy statistics, and the chart.
5. You can save a copy using **File → Save a copy in Drive** or upload the notebook to GitHub as part of the project.

The notebook is **standalone**: you do not need to upload `processor.py` to Colab.

## Option B — Windows local run, with a venv

Open **PowerShell** in the extracted project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\processor.py
python -m unittest discover -s tests -v
```

If PowerShell blocks activation, do not change system policy; you can use the venv interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\processor.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On macOS/Linux, replace the activation command with `source .venv/bin/activate` and run `python3 -m venv .venv` if `python` is unavailable.

The `.venv/` directory must **not** be committed to GitHub. Committing `requirements.txt` plus the instructions is how other people recreate your environment. To verify installed versions, use `python -m pip list` inside the venv.

## Results (provided sample)

| Metric | Result |
| --- | ---: |
| Raw CSV rows | 38 |
| Clean readings | 30 |
| Rejected rows | 8 |
| Average temperature | 26.82 °C |
| Average humidity | 61.23% |
| Readings triggering an alert condition | 14 |

Sensor breakdown is saved to `outputs/sensor_summary.csv`; the trend chart is `outputs/temperature_trend.png`.

## Upload to GitHub with real commit history

Create a **new empty** GitHub repository called `iot-sensor-data-processing`. Do **not** select “Initialize with README” (this project already has one). In the local project directory:

```bash
git init
git add data src requirements.txt .gitignore
git commit -m "Add raw sensor data and processing script"
git add notebooks tests outputs README.md
git commit -m "Add Colab notebook, tests, and results"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/iot-sensor-data-processing.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Authenticate when GitHub prompts you. If this is your first time using Git, configure your `user.name` and `user.email` using the instructions provided by Git. The two commits reflect separate genuine project stages; you can also make your own edits and commit them.

**Submission:** Share (1) the GitHub repo link and (2) the Google Colab notebook link, accessible to the instructor. If you save the notebook in Drive, set sharing to **Anyone with the link → Viewer** if allowed by your course rules; otherwise use the GitHub notebook as the submitted file. Verify both links open before submission.

## What this exercise teaches

1. CSV input/output using Python's standard library.
2. Data validation and cleaning with reusable functions.
3. Array-based calculations, NumPy boolean masking, and per-sensor grouping.
4. Reproducible dependencies (`venv` and `requirements.txt`).
5. Version control and sharing notebooks through GitHub and Colab.

**No real sensor data was collected.** All example data is fabricated for practice. The threshold checks are basic rule-based processing, **not** a trained machine-learning model.
