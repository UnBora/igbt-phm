# Phase 11 — Uncertainty in PHM

Phase 11 គឺជាការបន្តពី Phase 9 និង Phase 10 ហើយមានគំនិតសំខាន់មួយ៖

> **Prediction មួយតម្លៃមិនគ្រប់គ្រាន់សម្រាប់ PHM។ យើងក៏ត្រូវដឹងថា prediction នោះ “ប្រាកដប៉ុណ្ណា”។**

---

## 1. Point Prediction vs Uncertainty

ស្រមៃថា model មួយ predict៖

```text
Predicted RUL = 20 hours
```

នេះគឺជា **point prediction**។

ប៉ុន្តែយើងមិនដឹងថា 20 hours នេះមានភាពជឿជាក់កម្រិតណាទេ។

អាចជា៖

```text id="7x6zj1"
Case A:
Prediction = 20 hours
Uncertainty = ±1 hour

→ approximately 19–21 hours
```

ឬ៖

```text id="x1m6k8"
Case B:
Prediction = 20 hours
Uncertainty = ±10 hours

→ approximately 10–30 hours
```

ទាំងពីរមាន **same point prediction = 20 hours** ប៉ុន្តែ information សម្រាប់ maintenance decision ខុសគ្នាខ្លាំង។

---

# 2. ហេតុអ្វី Uncertainty សំខាន់ក្នុង PHM?

PHM មិនមែនគ្រាន់តែ៖

> “Model says 20 hours.”

ទេ។

Maintenance engineer អាចត្រូវសួរ៖

> “How confident are we?”

ឧទាហរណ៍៖

```text id="q3l6jz"
Prediction = 20 h

Narrow uncertainty
10? No
19 ─────── 20 ─────── 21
       relatively narrow

Wide uncertainty
10 ─────────── 20 ─────────── 30
          much wider
```

បើ maintenance threshold ជិត 20 hours នោះ uncertainty អាចមានឥទ្ធិពលលើ decision។

---

# 3. Prediction Interval

Concept មួយដែលសំខាន់គឺ **Prediction Interval (PI)**។

ជំនួសឱ្យ៖

$$
\hat y = 20
$$

យើងអាចមាន៖

$$
\hat y = 20,\quad PI=[17,23]
$$

មានន័យថា model ផ្តល់៖

```text id="1f7kqg"
Point prediction
      ↓
     20
      │
      ├───────────────┐
      │               │
     17               23
      └───────────────┘
       Prediction Interval
```

**ចំណាំ:** ការបកស្រាយ probability របស់ interval អាស្រ័យលើវិធីសាស្ត្រដែលប្រើដើម្បីបង្កើតវា។ មិនគួរបកស្រាយ interval ណាមួយថា “មាន 95% chance” ដោយស្វ័យប្រវត្តិទេ។

---

# 4. Uncertainty មិនមែន Error ដូចគ្នាទេ

ត្រូវបែងចែក concepts ពីរនេះ៖

### Prediction Error

បន្ទាប់ពីយើងដឹង actual value៖

$$
Error = y-\hat y
$$

ឧទាហរណ៍៖

```text
Actual = 18
Predicted = 20

Error = -2
```

### Uncertainty

គឺការបង្ហាញថា prediction មាន **range/uncertainty** ប៉ុន្មាន មុនពេល actual outcome ត្រូវបានដឹង។

```text
Prediction = 20
Interval = [17, 23]
```

ដូច្នេះ៖

```text
Error
→ How wrong was the prediction?

Uncertainty
→ How uncertain is the prediction?
```

---

# 5. ប្រភេទ Uncertainty សំខាន់ៗ

ក្នុង PHM ជាទូទៅយើងអាចគិតពី uncertainty ជាពីរប្រភេទធំៗ។

## A. Aleatoric Uncertainty

គឺ uncertainty ដែលកើតពី **intrinsic variability/noise in observations or process**។

ឧទាហរណ៍៖

```text id="m1ez9f"
Sensor noise
Measurement variation
Operating variability
Natural process variability
```

វាអាចនៅតែមាន ទោះ model ល្អក៏ដោយ។

---

## B. Epistemic Uncertainty

គឺ uncertainty ដែលពាក់ព័ន្ធនឹង **lack of knowledge/data**។

ឧទាហរណ៍៖

```text id="y8m0j6"
Very little training data
Few devices
Unseen operating condition
Limited degradation examples
```

នេះមានសារៈសំខាន់ខ្លាំងសម្រាប់ PHM ព្រោះ dataset ដែលមាន devices តិចអាចធ្វើឱ្យ model uncertainty ខ្ពស់។

---

# 6. ហេតុអ្វី IGBT Project របស់អ្នកមិនអាចបង្កើត RUL Interval ឥឡូវនេះ?

នេះគឺជា **readiness warning** របស់ Phase 11។

ពី Phase 8 យើងដឹងថា៖

```text
No defensible measured RUL target
             ↓
No verified cohort-wide EoL
             ↓
No trustworthy RUL labels
```

ដូច្នេះយើង **មិនគួរធ្វើ**៖

```text
IGBT data
   ↓
"Predicted RUL = 25 hours"
   ↓
"95% CI = 20–30 hours"
```

ព្រោះវានឹងបង្កើត appearance ថា RUL prediction មាន physical ground truth នៅពីក្រោយវា ខណៈដែល target មិនទាន់ defensible។

---

# 7. ដូច្នេះ Phase 11 ប្រើអ្វី?

វាប្រើ **small synthetic regression example**។

មានន័យថា data ត្រូវបានបង្កើតឡើងសម្រាប់ **learning purpose only**។

```text id="lq7j5w"
Synthetic data
      ↓
Simple regression
      ↓
Prediction
      ↓
Interval
      ↓
Learn uncertainty concept
```

វា **មិនមែន**៖

```text
IGBT measurement
      ↓
RUL
```

ហើយមិនមែន PHM result របស់ project ទេ។

---

# 8. Synthetic Example ងាយៗ

ស្រមៃថាយើងមាន regression data៖

```text
x → y

1 → 3
2 → 5
3 → 6
4 → 8
5 → 10
```

យើង fit regression model៖

$$
\hat y=b_0+b_1x
$$

បន្ទាប់មកសម្រាប់ \(x=6\) model អាចផ្តល់៖

```text id="c7l20w"
Point prediction
      ↓
      11
```

ហើយបង្កើត prediction interval៖

```text id="y7u8qq"
9 ─────────── 11 ─────────── 13
             ↑
          prediction
```

នេះគ្រាន់តែបង្ហាញ **concept**។

---

# 9. Calibration — ចំណុចសំខាន់

Phase 11 ប្រើពាក្យ៖

> **well-calibrated uncertainty**

Calibration មានន័យសាមញ្ញថា៖

> បើ model អះអាងថា interval របស់វាមាន coverage កម្រិតណាមួយ នោះនៅលើ repeated unseen cases coverage ដែលសង្កេតបានគួរតែសមស្របនឹងការអះអាងនោះ។

ឧទាហរណ៍ conceptually៖

```text id="6hrx6p"
100 test predictions

Prediction intervals
      ↓
Observed outcomes
      ↓
Check how often outcomes
fall inside intervals
```

ដូច្នេះ uncertainty មិនគួរគ្រាន់តែជា **លេខដែល model បង្កើតឡើង** ទេ។

ត្រូវ evaluate វាផងដែរ។

---

# 10. PHM Decision មាន Uncertainty ចូលរួម

ស្រមៃថា maintenance threshold = 20 hours។

### Prediction A

```text id="mm5wtr"
RUL = 25 h
Interval = [24, 26]
```

### Prediction B

```text id="m03lyc"
RUL = 25 h
Interval = [10, 40]
```

Point prediction ដូចគ្នា៖

```text
25 hours
```

ប៉ុន្តែ uncertainty ខុសគ្នាខ្លាំង។

ដូច្នេះ decision maker អាចត្រូវពិចារណា៖

```text
Prediction
+
Uncertainty
+
Maintenance threshold
+
Risk/cost
```

PHM ជាក់ស្តែងត្រូវការទាំងនេះ មិនមែន point estimate តែមួយទេ។

---

# 11. Phase 11 មិនមែន “Predict RUL” ទេ

នេះត្រូវចងចាំដូច Phase 10។

### Phase 10

```text
Can we prepare sequence data
for Deep Learning?
```

### Phase 11

```text
If a valid prediction exists,
how uncertain is it?
```

ប៉ុន្តែសម្រាប់ IGBT dataset របស់អ្នក៖

```text id="u4r6hr"
Valid RUL target ❌
       ↓
RUL model ❌
       ↓
RUL prediction ❌
       ↓
RUL uncertainty interval ❌
```

ដូច្នេះ Phase 11 គឺ **concept lesson** មិនមែនជាការបង្កើត PHM result។

---

# 12. Phase 8 → 9 → 10 → 11

អ្នកអាចចងចាំ sequence ទាំងនេះ៖

```text id="6i0h4e"
Phase 8
Define RUL
    ↓
Is EoL valid?
    ↓
Phase 9
ML readiness
    ↓
Is target valid?
    ↓
Phase 10
DL readiness
    ↓
Can sequence representation be prepared?
    ↓
Phase 11
Uncertainty
    ↓
How confident is the prediction?
```

ឬជា PHM pipeline ពេញ៖

```text id="t2d9gq"
Measurements
    ↓
Features
    ↓
Candidate HI
    ↓
Degradation
    ↓
BoL / EoL definition
    ↓
Valid RUL target
    ↓
Baseline ML
    ↓
Deep Learning
    ↓
Prediction
    ↓
Uncertainty
    ↓
Maintenance Decision
```

---

## ⭐ Main Lesson of Phase 11

> **A prediction without uncertainty can give an incomplete picture of risk.**

សម្រាប់ project របស់អ្នក៖

> **Phase 11 does not produce an IGBT RUL prediction or RUL interval. It uses synthetic regression data only to teach prediction intervals and uncertainty concepts, because the IGBT dataset still lacks a defensible measured RUL target.**

ចំណុចដែលគួរចាំបំផុត៖

**Point prediction → “What do we predict?”**

**Uncertainty → “How uncertain is that prediction?”**

**Calibration → “Can we trust the uncertainty estimate?”**

ហើយក្នុង PHM៖

**Prediction + Uncertainty → better information for risk-aware maintenance decisions.**
