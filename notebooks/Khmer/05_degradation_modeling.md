## Phase 7 — Degradation Modeling

Phase 7 គឺចាប់ផ្តើមយក **candidate feature** ពី Phase 5/6 មកមើលថា៖

> **“បើ device កំពុង aging តើ measurement/health-related feature នោះផ្លាស់ប្តូរតាមពេលវេលាយ៉ាងដូចម្តេច?”**

ប៉ុន្តែចំណុចសំខាន់បំផុតគឺ **កុំច្រឡំ trend ជាមួយ actual degradation**។

---

# 1. Degradation Modeling គឺជាអ្វី?

**Degradation** = ស្ថានភាពរបស់ device កាន់តែអន់ទៅៗ ដោយសារការខូចខាតកើនឡើង។

ឧទាហរណ៍សាមញ្ញ៖

```text
Healthy
   ↓
Aging
   ↓
Degradation
   ↓
Severe degradation
   ↓
Failure / EoL
```

យើងអាចមាន measurement មួយដែលផ្លាស់ប្តូរ៖

```text
Feature
  │
  │        •
  │      •
  │    •
  │  •
  │•
  └──────────────────→ Recorded Time
```

យើងអាច fit model មួយទៅលើ trend នេះ៖

$$
y = ax+b
$$

ដែល៖

* \(y\) = candidate feature
* \(x\) = recorded time
* \(a\) = slope
* \(b\) = intercept

នេះអាចប្រាប់យើងថា **feature កំពុងកើន ឬថយតាម recorded time ឬអត់**។

---

# 2. ប៉ុន្តែនេះមិនទាន់មានន័យថា “Degradation” ទេ

នេះជាចំណុចដែល Phase 7 ចង់ឱ្យយើងយល់។

ឧទាហរណ៍៖

```text
Feature increases
       │
       ├── Actual degradation ?
       │
       ├── Temperature change ?
       │
       ├── Supply voltage change ?
       │
       ├── Measurement drift ?
       │
       ├── Different acquisition setting ?
       │
       └── Stress protocol ?
```

ដូច្នេះ៖

> **Trend ≠ Proven degradation**

Phase 6 យើងបានសួរ៖

> “តើ feature នេះមាន behavior ដែលសមរម្យសម្រាប់ជា candidate HI ឬទេ?”

Phase 7 យើងបន្តសួរ៖

> “តើយើងអាចពិពណ៌នា trajectory របស់ candidate feature នេះតាម recorded time បានយ៉ាងដូចម្តេច?”

---

# 3. Degradation Modeling vs Diagnosis vs Prognosis vs RUL

នេះគឺជាផ្នែកសំខាន់ណាស់។

### A. Degradation Modeling

សំណួរ៖

> **How does a health-related measurement evolve over time?**

ឧទាហរណ៍៖

```text
Time ───────────────→

Feature
  │
  │       /
  │     /
  │   /
  │ /
  └─────────────────
```

យើង model trajectory របស់ feature។

---

### B. Diagnosis

សំណួរ៖

> **What is wrong with the device now?**

ឧទាហរណ៍៖

```text
Sensor data
     ↓
Diagnosis
     ↓
Bearing fault
or
Gate fault
or
Electrical fault
```

Diagnosis ផ្តោតលើ **current condition/fault**។

វាមិនមែនសួរ៖

> “នៅសល់ប៉ុន្មានម៉ោងទៀត?”

---

### C. Prognosis

សំណួរ៖

> **What will happen in the future?**

ឧទាហរណ៍៖

```text
Current State
      ↓
Model
      ↓
Future condition
      ↓
Expected degradation
      ↓
Future event
```

Prognosis ត្រូវការ model ដែលមានមូលហេតុគាំទ្រ និង uncertainty។

---

### D. RUL Prediction

RUL = **Remaining Useful Life**

សំណួរ៖

> **How much useful life remains before a defined EoL?**

ឧទាហរណ៍៖

```text
BoL                         EoL
 │                            │
 ▼                            ▼
Healthy ─── Aging ─── Degradation ─── Failure
             │
             │
          Current
             │
             └──────────────→ RUL
```

បើ EoL មិនទាន់កំណត់ យើងមិនអាចមាន RUL ដែលមានន័យច្បាស់បានទេ។

---

# 4. ហេតុអ្វី Phase 7 មិនធ្វើ RUL?

ព្រោះ dataset របស់យើងមិនទាន់មាន information គ្រប់គ្រាន់សម្រាប់បង្កើត RUL target ដែលមានភាពជឿជាក់។

ត្រូវដឹងយ៉ាងហោចណាស់៖

```text
BoL
 │
 ▼
Aging history
 │
 ▼
Current condition
 │
 ▼
EoL definition
 │
 ▼
RUL
```

ត្រូវកំណត់៖

* **BoL** = Beginning of Life
* **EoL** = End of Life
* Failure criterion
* Aging coordinate
* Censoring / incomplete observation

ដូច្នេះ Phase 7 **មិនបង្កើត RUL label** ទេ។

---

# 5. តើ Phase 7 នឹងធ្វើអ្វីជាក់ស្តែង?

យើងយក **one candidate feature per device** ពី Phase 5/6។

ឧទាហរណ៍៖

```text
Device 2
Device 3
Device 4
Device 5
```

ហើយមើល៖

```text
Recorded Time
      ↓
Candidate Feature
      ↓
Fit Linear Baseline
      ↓
Slope
      ↓
Describe Trend
```

Linear baseline៖

$$
y = ax+b
$$

ឧទាហរណ៍៖

```text
Feature
  │
  │            •
  │         •
  │      •
  │   •
  │ •
  └──────────────────→ time
          /
         /
        /
       Linear fit
```

---

# 6. ហេតុអ្វីប្រើ Linear Baseline?

មិនមែនដោយសារយើងជឿថា IGBT degradation គឺ **linear** ទេ។

វាគ្រាន់តែជា **simple descriptive baseline**។

វាជួយឱ្យយើងឆ្លើយសំណួរដំបូង៖

* តើ feature មាន upward trend?
* តើមាន downward trend?
* Trend ខ្លាំងប៉ុណ្ណា?
* Device នីមួយៗមាន behavior ដូចគ្នាឬទេ?
* Trend មាន variability ខ្លាំងឬទេ?

ឧទាហរណ៍៖

$$
y = 0.02x + 3
$$

មានន័យថា ក្នុង descriptive model នេះ feature មាន slope វិជ្ជមាន។

ប៉ុន្តែ **វាមិនមានន័យថា degradation កើនដោយ 0.02 units ក្នុងមួយ aging cycle ទេ** ព្រោះ \(x\) របស់យើងមិនមែនជា cycle count ឬ verified aging dose។

---

# 7. `timeEpoch` ត្រូវយល់ឱ្យច្បាស់

ក្នុង Phase 7៖

> **x-axis = within-device recorded clock time**

វាជា **time proxy** ប៉ុណ្ណោះ។

មិនមែន៖

```text
❌ Cycle count
❌ Number of thermal cycles
❌ Cumulative thermal dose
❌ Verified degradation amount
❌ EoL time
```

គឺ៖

```text
timeEpoch
   ↓
Recorded time
   ↓
Proxy for ordering observations
```

ដូច្នេះ ប្រសិនបើ graph បង្ហាញ៖

```text
Feature ↑
       /
      /
     /
    /
───┴──────────────→ timeEpoch
```

យើងអាចនិយាយថា៖

> “The candidate feature shows an increasing trend with recorded time.”

មិនគួរនិយាយថា៖

> “The device physically degraded linearly with aging.”

ព្រោះយើងមិនទាន់មាន evidence គ្រប់គ្រាន់។

---

# 8. តើ Linear Model ប្រាប់យើងអ្វី?

សម្រាប់ device មួយ៖

$$
y = ax+b
$$

### `a` = Slope

Slope ប្រាប់ direction និង rate នៃ **descriptive trend**។

```text
a > 0  → feature tends to increase
a < 0  → feature tends to decrease
a ≈ 0  → little linear trend
```

### `b` = Intercept

គឺ estimated value នៅពេល \(x=0\) ក្នុង model។

ក្នុង PHM context វាមិនចាំបាច់មាន physical meaning ទេ។

---

# 9. ត្រូវធ្វើ Device-by-Device

កុំយក device ទាំងអស់មកបញ្ចូលគ្នាភ្លាមៗ។

គួរមើល៖

```text
Device 2 ──→ Trend
Device 3 ──→ Trend
Device 4 ──→ Trend
Device 5 ──→ Trend
```

ហើយសួរ៖

> តើ trend របស់ device នីមួយៗមាន consistency ឬទេ?

ឧទាហរណ៍៖

```text
Device 2   ↗
Device 3   ↗
Device 4   ↘
Device 5   →
```

នេះគឺជាលទ្ធផលសំខាន់មួយ។

វាប្រាប់យើងថា **candidate feature មាន behavior ខុសគ្នារវាង devices**។

មិនគួរបង្ខំវាឱ្យក្លាយជា universal degradation model ទេ។

---

# 10. Flow ពី Phase 5 → Phase 7

នេះជាផ្លូវដែលអ្នកគួរចងចាំ៖

```text
Phase 5
Raw transient waveform
        ↓
Feature Extraction
        ↓
Candidate Features
        ↓
Phase 6
Health Indicator assessment
        ↓
Trend
Monotonicity
Variability
Stability
Physical plausibility
        ↓
Candidate HI
        ↓
Phase 7
Degradation Modeling
        ↓
Device-by-device trajectory
        ↓
Descriptive Linear Baseline
        ↓
Slope / Trend
        ↓
Interpret carefully
```

---

# 11. Phase 7 មិនទាន់ដល់ RUL

Overall PHM pipeline អាចមើលជា៖

```text
Raw Data
   ↓
Data Loading
   ↓
EDA
   ↓
Feature Engineering
   ↓
Health Indicator
   ↓
Degradation Modeling
   ↓
Prognosis
   ↓
RUL Prediction
   ↓
Maintenance Decision
```

ប៉ុន្តែ project របស់អ្នកនៅ Phase 7 គឺនៅត្រឹម៖

```text
        CURRENT PROJECT
              │
              ▼
Candidate Feature
              │
              ▼
Candidate HI
              │
              ▼
Descriptive Trend
              │
              ▼
Linear Baseline
              │
              ▼
Understand trajectory
```

មិនទាន់ទៅដល់៖

```text
❌ EoL prediction
❌ RUL prediction
❌ Failure threshold
❌ Maintenance decision
```

---

## 12. ចំណុចសំខាន់បំផុតសម្រាប់ Presentation

បើអ្នកត្រូវពន្យល់ Phase 7 នៅក្នុង presentation អាចចងចាំជា 4 ប្រយោគនេះ៖

> **Degradation modeling** studies how a health-related measurement evolves over time as damage accumulates.

> **Diagnosis** identifies the current fault or condition.

> **Prognosis** estimates future condition or events with uncertainty.

> **RUL prediction** estimates the remaining useful life until a defined End of Life.

ហើយសម្រាប់ dataset របស់អ្នក៖

> **Phase 7 uses a descriptive linear baseline on one candidate feature per device, with within-device recorded time used only as a time proxy. It does not create EoL or RUL labels.**

### សម្រាប់យល់ជាភាសាខ្មែរ

**Phase 7 មិនទាន់ព្យាករណ៍ថា IGBT នឹងខូចពេលណាទេ។** វាគ្រាន់តែយក candidate feature មួយ ហើយពិនិត្យថា feature នោះមាន **trend តាម recorded time** យ៉ាងដូចម្តេច។ បន្ទាប់មកប្រើ **linear model** ជា baseline ដើម្បីពិពណ៌នា trend នោះ។
