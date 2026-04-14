# HR Hub Notebooks

Data preparation, exploratory analysis, and attrition model training for the HR Hub platform.

## Setup

```bash
cd notebooks
uv sync
```

## Notebooks

### `db_seed.ipynb`

Seeds the SQLite database with generated employee data. Must be run **after** Alembic migrations have created the tables.

What it does:
1. Loads the raw attrition dataset from `mock-cloud/storage/data/raw/employee_attrition_raw.csv`
2. Cleans and renames columns to match the ORM schema
3. Loads the generated employee roster from `mock-cloud/storage/data/processed/employees.csv`
4. Joins employees to attrition records by department
5. Writes to the `employee` and `employee_info` tables in `mock-cloud/db/hr_hub.db`

Run via the Makefile (recommended — handles the full pipeline):
```bash
make reset-db   # delete-db → revision → migrate → seed
```

### `employee_attrition/attrition_eda.ipynb`

Exploratory data analysis on the HR Analytics / Job Prediction dataset. Covers feature distributions, correlation analysis, and attrition breakdown by department and salary tier.

Data source: [HR Analytics and Job Prediction](https://www.kaggle.com/datasets/mfaisalqureshi/hr-analytics-and-job-prediction/data) (Kaggle)

### `employee_attrition/attrition_modeling.ipynb`

Trains and evaluates a classification model to predict employee attrition risk. The trained model is the `SOTA_PATH` artifact consumed by the backend's `service/prediction.py` at startup.

## Scripts

### `generate_employees.py`

Generates a synthetic employee roster (`mock-cloud/storage/data/processed/employees.csv`) with realistic names, emails, departments, and equipment assignments. Run this if you need to regenerate the enriched employee data.

```bash
uv run python generate_employees.py
```

## Data layout

```
mock-cloud/storage/data/
├── raw/
│   └── employee_attrition_raw.csv      # original Kaggle dataset
└── processed/
    ├── employee_attrition_processed.csv # cleaned, renamed columns
    └── employees.csv                    # generated employee roster
```
