# Phase 9 — Baseline Machine Learning (Readiness Gate)

Phase 9 មានគំនិតសំខាន់មួយ៖

> **មិនមែនមាន dataset + features ហើយត្រូវ train Machine Learning model ភ្លាមៗទេ។**

មុនពេល train model ត្រូវពិនិត្យថា **target ដែលយើងចង់ predict មានន័យត្រឹមត្រូវឬអត់** និង **data split មិនមាន leakage**។

---

## 1. “Readiness Gate” មានន័យអ្វី?

**Readiness Gate** = ច្រកត្រួតពិនិត្យមុនចូលទៅ Machine Learning។

```text id="5w7j4k"
Data
 ↓
Features
 ↓
Target
 ↓
Is target valid?
 ↓
Is split valid?
 ↓
Is there leakage?
 ↓
       YES
        │
        ▼
Train ML model
```

បើ target មិន valid៖

```text id="h4ujv2"
Data
 ↓
Features
 ↓
❌ Invalid target
 ↓
STOP
```

នេះជាអ្វីដែល Phase 9 កំពុងបង្រៀន។

---

# 2. ហេតុអ្វី Notebook នេះមិន Train Model?

Phase 8 បានរកឃើញបញ្ហាសំខាន់ៗនៅក្នុង dataset។

### Problem 1 — EoL មិន uniform

មាន failure-like notes សម្រាប់៖

* Device 3
* Device 5

ប៉ុន្តែ៖

* Device 2 → គ្មាន explicit failure entry
* Device 4 → គ្មាន explicit failure entry

ដូច្នេះយើងមិនអាចសន្មត់ថា៖

```text id="0e8f4f"
Device 3 → EoL
Device 5 → EoL
Device 2 → ?
Device 4 → ?
```

មាន **uniform EoL definition** សម្រាប់ devices ទាំងអស់ទេ។

---

# 3. Problem 2 — `remaining_observed_hours` មិនមែន RUL ពិត

នេះគឺជា point សំខាន់បំផុត។

Target ដែលមាន៖

```text id="r7t8c5"
remaining_observed_hours
```

មានន័យថា៖

> តើនៅសល់ប៉ុន្មានម៉ោងទៀត រហូតដល់ **ចុងបញ្ចប់នៃ recorded data segment**?

មិនមែន៖

> តើនៅសល់ប៉ុន្មានម៉ោងទៀត រហូតដល់ **physical failure / verified EoL**?

ប្រៀបធៀប៖

```text id="j6w6x5"
Actual RUL

Current
  │
  ├───────────────→ Physical EoL
  │
  └──────── RUL ──────────→


remaining_observed_hours

Current
  │
  ├───────────────→ End of recorded data
  │
  └── observation horizon ──→
```

ដូច្នេះ៖

> **Observation horizon ≠ RUL**

---

# 4. ហេតុអ្វីបញ្ហានេះធ្ងន់?

Suppose model predict៖

$$
\hat y = 20\text{ hours}
$$

ហើយ actual `remaining_observed_hours` = 20 hours។

យើងអាចគិតថា៖

> “Model predicted RUL accurately!”

ប៉ុន្តែវាគ្រាន់តែបាន predict៖

> **time remaining until the dataset stops recording.**

មិនមែន physical failure ទេ។

---

# 5. បើ Train Model ឥឡូវនេះ នឹងមានអ្វីកើតឡើង?

អាច train models ដូចជា៖

```text id="a3mb4c"
Linear Regression
Random Forest
Gradient Boosting
XGBoost
```

Input៖

```text id="1b8ydo"
Voltage
Current
Temperature
Features
```

Target៖

```text id="7q6t3q"
remaining_observed_hours
```

Model អាច train បានតាម technical perspective។

ប៉ុន្តែបញ្ហាគឺ៖

```text id="e6h7xk"
Model
  ↓
Predicts observation horizon
  ≠
Predicts physical RUL
```

ដូច្នេះ MAE/RMSE អាចមើលទៅល្អ ប៉ុន្តែ **មិនអាចហៅវាថា RUL accuracy បានទេ**។

---

# 6. MAE / RMSE ក៏អាច misleading

ឧទាហរណ៍៖

```text
MAE  = 2.1 hours
RMSE = 3.5 hours
```

វាហាក់ដូចជា model ល្អ។

ប៉ុន្តែយើងត្រូវសួរជាមុន៖

> **2.1 hours error លើអ្វី?**

បើ target គឺ៖

```text
remaining_observed_hours
```

នោះ MAE = 2.1 hours មានន័យថា៖

> model មាន average error ប្រហែល 2.1 hours ក្នុងការទាយ **observation horizon**។

មិនមែន៖

> model ទាយ physical RUL ខុសតែ 2.1 hours។

---

# 7. Date vs `timeEpoch` ក៏មានបញ្ហា

Phase 9 ក៏រកឃើញថា៖

```text
MAT `date`
```

និង

```text
timeEpoch interpreted as Unix time
```

មិនស៊ីគ្នា។

វាខុសគ្នា **ជាច្រើនទសវត្សរ៍**។

នេះមានន័យថា យើងមិនគួរយក timestamp ទាំងពីរមក combine ដោយសន្មត់ថាវាជា clock ដូចគ្នាទេ។

Conceptually៖

```text id="pr7f8g"
date
  │
  └───────┐
          │
          ├── Are they the same clock?
          │
timeEpoch ┘
          ↓
       UNKNOWN
```

ត្រូវ **resolve និង document** មុននឹងប្រើវាសម្រាប់ event-time alignment ឬ RUL។

---

# 8. Machine Learning Leakage គឺជាអ្វី?

**Data leakage** = information ពី target/future ឬ information ដែលមិនគួរមាននៅពេល prediction ត្រូវបានបញ្ចូលទៅ model។

ក្នុង PHM វាសំខាន់ខ្លាំង ព្រោះយើងចង់ simulate៖

> **នៅពេល actual operation ខ្ញុំមាន information ត្រឹមនេះ → តើខ្ញុំអាច predict future RUL បានទេ?**

មិនមែន៖

```text id="e2j2t5"
Give model future information
        ↓
Predict future
```

នោះទេ។

---

# 9. Example នៃ Leakage

ស្រមៃថា៖

```text id="1v1wfw"
Device history
──────────────────────────────→ time

Past                  Future
  │                      │
  ▼                      ▼
Features             Failure info
```

បើ feature របស់ model មាន information ដែលបានមកពី future ឬ EoL information ដែលមិនអាចដឹងនៅ prediction time៖

```text id="02f2e9"
Future information
       ↓
     Model
       ↓
   Prediction
```

Model អាច score ល្អខ្លាំង ប៉ុន្តែវាមិន represent real deployment ទេ។

---

# 10. តើ “split matches deployment” មានន័យអ្វី?

សម្រាប់ PHM យើងត្រូវគិតពី **time/order** និង **device identity**។

ឧទាហរណ៍មិនគួរធ្វើ random split ដោយមិនគិតពី structure៖

```text id="x2xj6v"
Random rows
 ├── Train
 ├── Train
 ├── Test
 ├── Train
 └── Test
```

ព្រោះ rows ពី device/time series ដូចគ្នាអាចមាន correlation ខ្លាំង។

Conceptually យើងចង់ simulate៖

```text id="w9e6eu"
Past observations
       ↓
     TRAIN
       │
       ▼
Future / unseen condition
       ↓
      TEST
```

ប៉ុន្តែ exact split strategy ត្រូវអាស្រ័យលើ intended deployment និង dataset structure។

---

# 11. តើត្រូវដោះស្រាយអ្វីមុន Train RUL Model?

Phase 9 ប្រាប់យើងថា ត្រូវ resolve៖

### ① BoL

តើ **Beginning of Life** នៅឯណា?

```text
BoL
 ↓
Aging exposure
 ↓
Current observation
```

### ② EoL

តើ **End of Life** ត្រូវកំណត់ដោយអ្វី?

```text
Performance limit?
Failure event?
Electrical criterion?
Other physical criterion?
```

### ③ Failure criteria

តើអ្វីជាចំណុចដែលយើងហៅថា failure?

### ④ Event-time alignment

តើ `date`, `timeEpoch`, aging records និង failure events ប្រើ clock ដូចគ្នាឬទេ?

### ⑤ Censoring

តើ device ខ្លះឈប់សង្កេតមុន failure ឬទេ?

```text
Observed failure
       vs
Right-censored observation
```

ទាំងនេះត្រូវច្បាស់មុនបង្កើត RUL labels។

---

# 12. Phase 9 គឺជា “STOP” មិនមែន “FAIL”

ចំណុចនេះសំខាន់សម្រាប់ presentation។

Phase 9 មិនមែន៖

> “We cannot do Machine Learning.”

ទេ។

វាគឺ៖

> **“The dataset is not yet ready for defensible RUL Machine Learning.”**

ន័យថា៖

```text id="pl5xw3"
Dataset
   ↓
Feature Engineering ✓
   ↓
Candidate HI ✓
   ↓
Degradation analysis ✓
   ↓
RUL definition
   ↓
❌ Target not sufficiently defensible
   ↓
READINESS GATE
   ↓
STOP BEFORE ML
```

នេះជាវិធីសាស្ត្រដែលមាន scientific discipline ជាងការបង្ខំ train model ដើម្បីបាន RMSE មួយ។

---

# 13. Phase 7 → 8 → 9

អ្នកអាចចងចាំជា sequence នេះ៖

```text id="n0k5a7"
Phase 7
Degradation Modeling
"What changes over time?"
          ↓
Phase 8
RUL Definition
"What exactly is EoL?"
          ↓
Phase 9
ML Readiness
"Do we have a valid target?"
          ↓
       YES?
      /    \
    YES     NO
     ↓       ↓
   Train    Resolve
    ML      dataset/labels
```

---

## ⭐ Main lesson of Phase 9

**PHM មិនមែន៖**

```text
Dataset → Train XGBoost → RMSE → Call it RUL
```

ទេ។

វាគួរតែជា៖

```text
Dataset
   ↓
Understand measurements
   ↓
Feature Engineering
   ↓
Validate candidate HI
   ↓
Understand degradation
   ↓
Define BoL
   ↓
Define EoL
   ↓
Define valid RUL
   ↓
Check censoring
   ↓
Check leakage
   ↓
Define deployment-matched split
   ↓
ONLY THEN
   ↓
Machine Learning
   ↓
RUL Prediction
```

### សម្រាប់ NASA IGBT project របស់អ្នក

**Phase 9 conclusion គឺ៖**

> Dataset មាន data សម្រាប់ **exploration, feature engineering, candidate HI analysis, និង degradation analysis** ប៉ុន្តែ RUL Machine Learning មិនទាន់គួរធ្វើ ដោយសារ **verified EoL, uniform failure criteria, event-time alignment, និង censoring status** មិនទាន់ត្រូវបានកំណត់យ៉ាង defensible។

នេះក៏ជាមូលហេតុដែល `remaining_observed_hours` **មិនគួរត្រូវបានបង្ហាញជា RUL ground truth**។
