# NASA IGBT PHM learning project

This project is a hands-on, progressive study of PHM using the NASA IGBT
Accelerated Aging dataset. We will establish the experiment structure and
measurement meaning before attempting degradation analysis or RUL prediction.

## Start here: Phase 1 — Dataset Understanding

The extracted dataset is under `data/raw/IGBTAgingData_04022009/`. No original
ZIP file was found under `data/raw/` during the initial inspection. The
exploration notebook checks again and inventories the extracted files without
modifying them:

1. Create and activate an environment (Python 3.10 or newer):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Open [`notebooks/01_data_exploration.ipynb`](notebooks/01_data_exploration.ipynb)
   in VS Code, select the `.venv` Python interpreter/kernel, and run cells in
   order.
3. Review the worksheet and MAT metadata and answer the questions at the end of
   the notebook before moving to data loading.

The extracted archive contains multiple experiments and file types. Its
documentation reports missing transient measurements, collector-current drift,
and improperly scaled steady-state measurements in the square-gate-plus-SMU
aging data. The notebook highlights these limitations and the aging-log notes;
signal fields are not assumed to have valid units or to constitute failure
labels.

## Phase 2 — Data Loading

After completing the Phase 1 notebook, work through
[`notebooks/02_data_loading.ipynb`](notebooks/02_data_loading.ipynb). It loads
the actual steady-state records from the ten MAT files in the Device 2–5
square-gate aging folder, retains `check` and other file segments with source
identifiers, and walks through DataFrame shape, types, missingness, numeric
descriptions, and per-file timestamp intervals. Run the notebook cells in order.
It writes the extracted steady-state table to
`data/processed/aging_steady_state_observations.csv`; the nested original MAT
files remain unchanged. The table is not a lossless replacement for the MAT
files and excludes the separate transient waveforms.

## Phase 3 — Exploratory Data Analysis

After loading the Phase 2 table, continue with
[`notebooks/03_exploratory_data_analysis.ipynb`](notebooks/03_exploratory_data_analysis.ipynb).
It plots selected signals over recorded time without connecting file segments,
examines populated-channel distributions, compares selected values by source
file, and visualizes pairwise correlations. Each plot includes a PHM question
and cautions against mistaking controlled temperature/supply changes,
measurement drift, or scale problems for degradation. Figures are saved under
`results/figures/`. This phase does not clean observations, select a Health
Indicator, create RUL targets, or train models.

## Phase 4 — Signal Processing

After EDA, use [`notebooks/04_signal_processing.ipynb`](notebooks/04_signal_processing.ipynb)
to compare the irregular low-speed steady-state record cadence with the
per-capture sample interval in the high-speed transient MAT records. The
notebook demonstrates a deliberately illustrative low-pass filter and
event-window selection, explains the risks of per-record normalization, and
checks the actual frequency-domain arrays before deciding whether FFT analysis
is warranted. It does not save transformed signals, calculate spectral PHM
features, clean observations, or create RUL targets. Demonstration figures are
saved under `results/figures/`.

## Phase 5 — Feature Engineering

After signal processing, work through
[`notebooks/03_feature_engineering.ipynb`](notebooks/03_feature_engineering.ipynb).
This phase extracts exploratory time-domain descriptors from each available
high-speed transient capture: mean, standard deviation, RMS, extrema,
peak-to-peak, skewness, excess kurtosis, and crest factor. It keeps device/file
provenance and capture timing/sampling metadata, and discusses which channels
are context versus candidate degradation-sensitive measurements. It does not
combine transients with steady-state records, claim a validated Health
Indicator, or create RUL labels.

The notebook saves `data/features/transient_candidate_features.csv` and
figures under `results/figures/`. It deliberately omits FFT-derived features:
the stored frequency arrays are empty, while the captures are short switching
events with varying sample intervals. Voltage peak-to-peak is treated only as
a whole-capture candidate descriptor, not as an aligned switching overshoot or
proof of degradation. Read the experiment caveats before interpreting either
the feature table or its plots.

## Phase 6 — Health Indicator

After feature engineering, work through
[`notebooks/04_health_indicator.ipynb`](notebooks/04_health_indicator.ipynb).
It teaches the difference between a feature and a Health Indicator, then
compares physically plausible transient candidates using per-device trends,
Spearman monotonicity, robust slopes, trend-residual scatter, and sensitivity
to sampling/file groups. The notebook treats recorded clock time only as a
proxy, excludes `check` captures from aging-trend calculations, and does not
declare a single best HI. It explains why voltage peak-to-peak merits
mechanism-based follow-up but is not an event-aligned overshoot; it also
highlights current drift and gate-drive/context confounding. No failure label,
HI threshold, composite score, or RUL target is created.

## Phase 7 — Degradation Modeling

After HI screening, work through
[`notebooks/05_degradation_modeling.ipynb`](notebooks/05_degradation_modeling.ipynb).
It distinguishes degradation modeling from diagnosis, prognosis, and RUL
prediction, surveys simple and stochastic model families, and implements only
a per-device linear-regression baseline for a candidate voltage feature. A
chronological holdout illustrates later-capture fit; recorded clock time is
explicitly only a proxy. The fitted slopes and errors are not damage rates or
RUL accuracy, and no RUL labels or model artifacts are produced. Resolve the
BoL/EoL/failure definition in Phase 8 before considering RUL prediction.

## Hold off on the existing RUL prototype

An earlier prototype remains in `src/rul.py` and
[`notebooks/05_rul_baseline.ipynb`](notebooks/05_rul_baseline.ipynb). It uses
time remaining until the last recorded observation as a proxy target. That is
not verified physical RUL. The dataset has failure-like aging-log notes for
Devices 3 and 5, but no uniform failure criterion/label for all four devices,
and the MAT date text conflicts with `timeEpoch` interpreted as Unix time.
Do not use the prototype's metrics or model as a PHM conclusion.

## Phase 8 — RUL Definition

Before creating RUL labels, work through
[`notebooks/06_rul_definition.ipynb`](notebooks/06_rul_definition.ipynb).
It examines the available BoL/EoL and failure evidence, explains censoring, and
checks the recorded time fields. The log records latch-up for Device 3 and
inability to draw current for Device 5, but Devices 2 and 4 have no explicit
failure note in this experiment log. The records do not provide a cohort-wide
verified EoL target. In particular, MAT date text and numeric `timeEpoch`
values disagree by decades when the latter is read as Unix time. Therefore
this phase creates no RUL labels; any future assumed EoL must be named and
documented as an assumption, not represented as measured failure.

## Phase 9 — Baseline Machine Learning readiness

[`notebooks/07_baseline_machine_learning.ipynb`](notebooks/07_baseline_machine_learning.ipynb)
explains data leakage, deployment-appropriate chronological/device-held-out
splits, baseline model choices, and MAE/RMSE. It intentionally fits no models:
Phase 8 did not establish reliable measured RUL targets, so reporting metrics
now would measure prediction of an observation-horizon proxy rather than RUL.

## Phase 10 — Deep Learning readiness

[`notebooks/08_deep_learning.ipynb`](notebooks/08_deep_learning.ipynb)
teaches sequence creation, sliding windows, train-only normalization,
sequence-to-one prediction, LSTM/GRU, and later CNN/CNN-LSTM/Transformer
options for PHM. It demonstrates input-window preparation from real
transient-feature captures without generating targets or training a neural
network. Since the Phase 9 RUL baseline has not been justified or trained, this
phase is educational only; do not interpret its windows as RUL predictions.

## Phase 11 — Uncertainty

[`notebooks/09_uncertainty.ipynb`](notebooks/09_uncertainty.ipynb) teaches
point predictions, confidence versus prediction intervals, and aleatoric
versus epistemic uncertainty. A clearly labeled synthetic regression example
illustrates the interval distinction; it is not IGBT data. The notebook
discusses Monte Carlo Dropout, ensembles, probabilistic/survival models, and
calibration checks as later options. It reports no numeric IGBT RUL interval
because Phase 8 did not establish a valid RUL target.

## Phase 12 — Explainability

[`notebooks/10_explainability.ipynb`](notebooks/10_explainability.ipynb)
teaches model interpretation, built-in feature importance, permutation
importance, and SHAP, including PHM-specific risks such as correlated
features, stress-protocol shortcuts, and mistaking predictive attribution for
causality. A synthetic Random Forest example demonstrates held-out permutation
importance; it is not an IGBT health model. The notebook does not report
importance for actual IGBT RUL because no justified RUL model has been trained.

When processing is eventually justified, keep raw files unchanged and write
processed data, features, figures, models, and evaluation results to their
corresponding `data/processed/`, `data/features/`, `results/figures/`,
`models/`, and `results/metrics/` folders.