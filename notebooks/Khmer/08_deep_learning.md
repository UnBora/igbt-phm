# Phase 10 — Deep Learning for PHM

Phase 10 គឺជាការបន្តពី Phase 9 ប៉ុន្តែមានចំណុចសំខាន់មួយ៖

> **Deep Learning មិនមែនជាជំហានដែលត្រូវធ្វើដោយស្វ័យប្រវត្តិបន្ទាប់ពី Feature Engineering ទេ។ ត្រូវមាន valid target និង baseline ជាមុនសិន។**

---

## 1. ហេតុអ្វីមិន Train LSTM/GRU?

នៅ Phase 9 យើងបានរកឃើញថា៖

```text
No reliable RUL target
        ↓
No valid supervised baseline
        ↓
No meaningful baseline performance
        ↓
        ❌
LSTM / GRU training
```

សម្រាប់ dataset នេះ៖

* មិនមាន **verified EoL** សម្រាប់ devices ទាំងអស់
* Failure criteria មិនទាន់ uniform
* `date` និង `timeEpoch` មាន conflict
* `remaining_observed_hours` មិនមែន verified physical RUL
* ដូច្នេះមិនមាន **defensible RUL target**

ហេតុនេះ Phase 10 **មិន train LSTM ឬ GRU ទេ**។

---

# 2. Deep Learning ត្រូវការអ្វី?

សម្រាប់ supervised PHM problem យើងអាចគិតជា៖

```text
Raw Data
   ↓
Features / Sequences
   ↓
Valid Target
   ↓
Baseline ML
   ↓
Evaluate baseline
   ↓
Deep Learning
```

ឧទាហរណ៍ RUL៖

```text
Input
 ├── Voltage
 ├── Current
 ├── Temperature
 └── Other features
       ↓
   LSTM / GRU
       ↓
   Predicted RUL
```

ប៉ុន្តែ **Predicted RUL** មានន័យតែបើ training target គឺ RUL ពិតប្រាកដ។

---

# 3. LSTM និង GRU ប្រើសម្រាប់អ្វី?

**LSTM = Long Short-Term Memory**

**GRU = Gated Recurrent Unit**

ទាំងពីរជា neural-network architectures ដែលអាច process **sequential/time-series data**។

ឧទាហរណ៍៖

```text
Time 1 → Time 2 → Time 3 → Time 4 → Time 5
  │         │         │         │         │
  ▼         ▼         ▼         ▼         ▼
Feature   Feature   Feature   Feature   Feature
  │         │         │         │         │
  └──────────── LSTM / GRU ───────────────┘
                       ↓
                  Prediction
```

វាមានប្រយោជន៍ពេល **order និង temporal dependency** របស់ data មានសារៈសំខាន់។

---

# 4. Phase 10 កំពុងបង្រៀនអ្វី បើមិន Train Model?

វាកំពុងបង្រៀន **data representation** និង **architecture preparation**។

ជាពិសេស៖

### ① Chronological sequence windows

### ② Train-only normalization

### ③ Input tensor construction

ប៉ុន្តែ៖

```text
Input Tensor
     ≠
Trained Model
```

---

# 5. Sequence Window គឺជាអ្វី?

Suppose យើងមាន feature តាមពេល៖

```text
t1   t2   t3   t4   t5   t6   t7   t8
│    │    │    │    │    │    │    │
10   12   13   15   17   18   20   21
```

យើងអាចបង្កើត window មាន length = 4៖

```text
Window 1
[t1, t2, t3, t4]

Window 2
[t2, t3, t4, t5]

Window 3
[t3, t4, t5, t6]

Window 4
[t4, t5, t6, t7]

Window 5
[t5, t6, t7, t8]
```

នេះហៅថា **chronological sequence windows**។

---

# 6. ហេតុអ្វីត្រូវ Chronological?

ព្រោះ PHM មាន concept នៃ៖

```text
Past → Present → Future
```

យើងមិនគួររៀប sequence randomly ទេ។

ឧទាហរណ៍៖

```text
Correct:
t1 → t2 → t3 → t4 → t5

Wrong:
t4 → t1 → t5 → t2 → t3
```

LSTM/GRU ត្រូវការ temporal order ដើម្បីរៀនពី sequence។

---

# 7. Input Tensor គឺជាអ្វី?

នៅក្នុង Machine Learning ធម្មតា យើងអាចមាន៖

```text
Row 1 → [feature1, feature2, feature3]
Row 2 → [feature1, feature2, feature3]
```

ប៉ុន្តែ sequence model ត្រូវការ **3-dimensional tensor** ជាញឹកញាប់៖

$$
(\text{samples},\text{timesteps},\text{features})
$$

ឧទាហរណ៍៖

```text
(samples = 100,
 timesteps = 20,
 features = 8)
```

មានន័យថា៖

* `100` = 100 sequence windows
* `20` = observation ក្នុងមួយ window
* `8` = features ក្នុងមួយ observation

Conceptually៖

```text
100 windows
    │
    ├── Window 1
    │    ├── t1 → 8 features
    │    ├── t2 → 8 features
    │    ├── ...
    │    └── t20 → 8 features
    │
    ├── Window 2
    │    └── ...
    │
    └── Window 100
```

នេះហើយជា **input tensor**។

---

# 8. Train-only Normalization

នេះជាចំណុចសំខាន់សម្រាប់ **data leakage prevention**។

Suppose feature values:

```text
Train data
10, 12, 15, 18, 20

Test data
22, 25, 30
```

យើង fit normalization parameters ពី **training data only**។

ឧទាហរណ៍ Standardization៖

$$
z=\frac{x-\mu_{train}}{\sigma_{train}}
$$

ដែល៖

* \(\mu_{train}\) = mean ពី training data
* \(\sigma_{train}\) = standard deviation ពី training data

បន្ទាប់មកយក parameters ដដែលទៅ transform validation/test។

```text
TRAIN
  ↓
Calculate mean/std
  ↓
Fit scaler
  ↓
Transform TRAIN
  │
  ├──────────────→ Transform VALIDATION
  │
  └──────────────→ Transform TEST
```

មិនគួរធ្វើ៖

```text
TRAIN + TEST
      ↓
Calculate mean/std
      ↓
Normalize
```

ព្រោះ test information បានចូល training process → **leakage**។

---

# 9. តើ Phase 10 មាន Output អ្វី?

Output របស់ phase នេះគឺ៖

> **Input tensor**

មិនមែន៖

```text
❌ RUL prediction
❌ LSTM model
❌ GRU model
❌ Neural-network accuracy
❌ MAE/RMSE
```

គឺ៖

```text
IGBT transient captures
        ↓
Feature sequences
        ↓
Chronological windows
        ↓
Train-only normalization
        ↓
Input Tensor
```

---

# 10. ហេតុអ្វី “Actual IGBT transient-feature captures” សំខាន់?

Project នេះមិនបានបង្កើត fake data ដើម្បីសាក LSTM ទេ។

យើងប្រើ **actual transient-feature captures** ពី dataset។

ឧទាហរណ៍៖

```text
Capture 1
 ├─ mean
 ├─ std
 ├─ RMS
 ├─ peak-to-peak
 └─ ...

Capture 2
 ├─ mean
 ├─ std
 ├─ RMS
 ├─ peak-to-peak
 └─ ...

Capture 3
 └─ ...
```

បន្ទាប់មករៀបតាម chronological order៖

```text
Capture 1 → Capture 2 → Capture 3 → ...
```

ហើយបង្កើត sequence windows។

---

# 11. ប៉ុន្តែ Sequence មិនស្មើ RUL Dataset

នេះក៏សំខាន់ណាស់។

យើងអាចមាន៖

```text
Valid sequence
      ↓
Input tensor ✓
```

ប៉ុន្តែមិនមាន៖

```text
Valid EoL
      ↓
Valid RUL target
```

ដូច្នេះ៖

```text
Input tensor ✓
       +
RUL target ❌
       =
Cannot train supervised RUL model
```

---

# 12. Deep Learning ត្រូវការអ្វីមុន?

Phase 10 ប្រាប់យើងថា Deep Learning គួរតែចាប់ផ្តើមនៅពេលមាន៖

### 1. Valid target

ឧទាហរណ៍៖

```text
RUL
```

ដែលមាន physical meaning។

### 2. Time alignment

```text
BoL
 ↓
Aging time
 ↓
Observation
 ↓
EoL
```

ត្រូវ align បានត្រឹមត្រូវ។

### 3. Baseline performance

ដំបូងត្រូវដឹងថា simple model ធ្វើបានយ៉ាងដូចម្តេច។

```text
Linear / RF / Gradient Boosting
             ↓
         Baseline
             ↓
       Evaluate
             ↓
      Is DL justified?
```

### 4. Independent validation

Model មិនគួរត្រូវបាន evaluate តែលើ data ដែលស្រដៀង training data ខ្លាំងពេកទេ។

### 5. Adequate device/run counts

PHM data មាន **device-to-device variability** ខ្លាំង។

មាន devices តិចពេក អាចធ្វើឱ្យ neural network រៀន pattern របស់ device ជាក់លាក់ ជំនួសឱ្យរៀន degradation behavior ទូទៅ។

---

# 13. Why “More Complex” ≠ “Better”

នេះជាមេរៀនសំខាន់មួយ។

```text
Linear Regression
       ↓
Random Forest
       ↓
Gradient Boosting
       ↓
LSTM / GRU
```

មិនមានន័យថា៖

> LSTM/GRU ត្រូវតែ better ជាង Linear Regression។

Model complexity គួរត្រូវ justified ដោយ៖

* amount of data
* temporal structure
* target quality
* baseline performance
* validation design
* deployment requirement

បើ target ខុស៖

```text
Bad Target
    ↓
Simple ML → Bad result
    ↓
Deep Learning → Still bad target
```

Deep Learning មិនអាចជួសជុល **invalid labels** បានទេ។

---

# 14. Phase 9 → Phase 10

ចងចាំជា៖

```text
Phase 9
"Is ML ready?"
       ↓
No valid RUL target
       ↓
STOP
       ↓
Phase 10
"Can we prepare sequential representation?"
       ↓
Create chronological windows
       ↓
Train-only normalization
       ↓
Input Tensor
       ↓
NO MODEL TRAINING
```

---

# ⭐ Main Lesson

Phase 10 មិនមែនមានគោលបំណងបង្ហាញថា **LSTM/GRU អាច predict RUL បាន** ទេ។

វាបង្រៀនថា៖

> **Deep Learning for PHM should come after the PHM problem itself is well-defined.**

សម្រាប់ project របស់អ្នក៖

```text
Raw IGBT data
      ↓
Phase 5: Features
      ↓
Phase 6: Candidate HI
      ↓
Phase 7: Degradation trend
      ↓
Phase 8: RUL definition
      ↓
Phase 9: ML readiness
      ↓
Phase 10: DL representation
      ↓
      ⛔
No RUL training yet
```

ហើយ **Input Tensor ≠ PHM Predictor**។

នៅពេលក្រោយ ប្រសិនបើអាចកំណត់ **BoL + EoL + failure criteria + time alignment + censoring + valid RUL labels** បាន ហើយមាន baseline និង validation design ដែលត្រឹមត្រូវ ទើបមានហេតុផលក្នុងការបន្តទៅ៖

```text
Input sequences
      ↓
LSTM / GRU
      ↓
RUL prediction
      ↓
Evaluation
      ↓
Independent validation
```
