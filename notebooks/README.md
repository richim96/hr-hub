# HR Hub Notebooks

Data preparation, exploratory analysis, and attrition model training for the HR Hub platform.

## Setup

```bash
cd notebooks
uv sync
```

## Notebooks

### 1. `db_seed.ipynb`

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

---

### 2. `employee_attrition/attrition_eda.ipynb`

Exploratory data analysis on the [HR Analytics / Job Prediction](https://www.kaggle.com/datasets/mfaisalqureshi/hr-analytics-and-job-prediction/data) dataset (Kaggle).

**Dataset:** 14,999 employees, 9 features, no missing values. Overall attrition rate: **23.8%**.

#### Key findings

`SatisfactionScore` is the dominant signal — employees who left average a satisfaction score of 0.44, versus 0.67 for those who stayed. The effect is monotonic: the lowest satisfaction band (0–0.2) sees >60% attrition.

Categorical features show large, interpretable gaps:

| Feature | Group | Attrition rate |
|---|---|---|
| Salary | low | 30% |
| Salary | medium | 20% |
| Salary | high | 7% |
| ReceivedPromotion | no | 24% |
| ReceivedPromotion | yes | 6% |
| WorkAccidents | no | 27% |
| WorkAccidents | yes | 8% |

Tenure and project load show **non-monotonic** patterns — very high attrition at 5–6 years and then near-zero for longer-tenured employees, and a U-shaped curve across project counts (employees with 2 or 7 projects leave at much higher rates than those with 3–4). `LastEvaluation` has a bimodal attrition distribution, suggesting both low performers and high performers leave, but for different reasons.

Pearson correlations with attrition are modest for all features. The main modeling implication is that linear models will underfit — tree-based approaches that can capture thresholds and interactions are the right default.

---

### 3. `employee_attrition/attrition_modeling.ipynb`

Trains and evaluates classification models to predict attrition risk. The exported artifact is consumed by the backend's `service/prediction.py` at startup.

#### Models evaluated

Six models were compared on the held-out test set (80/20 stratified split):

| Model | ROC-AUC | Avg. Precision | Recall | F1 | Brier score |
|---|---|---|---|---|---|
| Stacked ensemble (LR + RF + HGB) | 0.9937 | 0.9901 | **0.9692** | 0.9645 | 0.0147 |
| **Hist. gradient boosting** | **0.9947** | **0.9902** | 0.9678 | **0.9678** | **0.0142** |
| Random forest | 0.9903 | 0.9852 | 0.9202 | 0.9494 | 0.0217 |
| Decision tree | 0.9611 | 0.8382 | 0.9440 | 0.8736 | 0.0598 |
| Logistic regression | 0.8339 | 0.5034 | 0.7983 | 0.6226 | 0.1689 |
| Dummy baseline | 0.5018 | 0.2386 | 0.2437 | 0.2422 | 0.3630 |

`HistGradientBoostingClassifier` was selected over the stacked ensemble — essentially identical metrics at a fraction of the complexity.

#### Calibration

The selected model was wrapped in `CalibratedClassifierCV(method="isotonic", cv=5)` so that output probabilities are true estimates — a predicted risk of 0.80 means approximately 80% probability of attrition, not just a relative ranking.

| | ROC-AUC | Avg. precision | Brier score |
|---|---|---|---|
| Uncalibrated | 0.9947 | 0.9902 | 0.0142 |
| **Calibrated** | 0.9944 | 0.9900 | **0.0119** |

Calibration marginally reduces discriminative performance while materially improving probability reliability (Brier score −16%).

#### Feature importance

Permutation importance (ROC-AUC drop, averaged over 10 repeats) on the held-out test set:

```
SatisfactionScore   ████████████████████  19.9%
YearsAtCompany      ███████               7.2%
ActiveProjects      ████                  4.2%
AvgMonthlyHours     ███                   3.0%
LastEvaluation      ██                    2.1%
Salary              <1%
Department          <1%
WorkAccidents       <1%
ReceivedPromotion   <1%
```

`SatisfactionScore` alone accounts for roughly 20 percentage points of ROC-AUC — clearly the strongest signal. Structural features (tenure, project load, hours) contribute meaningfully; compensation and HR-process features have negligible marginal impact once the others are accounted for.

#### Exported artifact

`mock-cloud/storage/models/attrition_classifier_artifact.joblib` — calibrated `HistGradientBoostingClassifier` pipeline. Set `SOTA_PATH` to this path to enable the backend's prediction endpoints.

## Scripts

### `generate_employees.py`

Generates a synthetic employee roster (`mock-cloud/storage/data/processed/employees.csv`) with realistic names, emails, departments, and equipment assignments. Run this if you need to regenerate the enriched employee data.

```bash
uv run python generate_employees.py
```

## Data layout

```
mock-cloud/storage/
├── data/
│   ├── raw/
│   │   └── employee_attrition_raw.csv          # original dataset
│   └── processed/
│       ├── employee_attrition_processed.parquet # cleaned, renamed columns
│       ├── employee_attrition_encoded.parquet   # label-encoded for modeling
│       └── employees.csv                        # generated employee roster
└── models/
    └── attrition_classifier_artifact.joblib     # exported SOTA pipeline
```
