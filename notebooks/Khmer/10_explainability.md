## Phase 12 — Explainability for PHM

**Explainability** មានន័យថា យើងព្យាយាមយល់ថា **ហេតុអ្វី model បានធ្វើ prediction មួយ** និង **feature ណាខ្លះដែល model ប្រើសម្រាប់ prediction នោះ**។

ក្នុង PHM វាសំខាន់ជាពិសេស ព្រោះ prediction អាចពាក់ព័ន្ធនឹងការសម្រេចចិត្តថា៖

* តើគួរ **inspect** ម៉ាស៊ីនឬទេ?
* តើគួរ **derate** operating condition ឬទេ?
* តើត្រូវរៀបចំ **spare parts** ឬទេ?
* តើអាចបន្ត **operating equipment** បានឬទេ?

---

# 1. Explainability មានន័យដូចម្តេច?

ស្រមៃថា model ទទួលបាន features:

```text
Temperature
Voltage Peak
Current RMS
Voltage RMS
Temperature Variation
```

ហើយ model ប្រាប់ថា:

```text
Predicted condition = High degradation
```

Engineer មិនគួរមើលតែ result នោះទេ។ គេចង់ដឹងថា៖

```text
Why?

Temperature      ────────┐
Voltage Peak      ────────┤
Current RMS       ────────┼──> PHM Model ──> Prediction
Voltage RMS       ────────┤
Temperature Var.  ────────┘
```

**Explainability** ជួយឆ្លើយសំណួរ៖

> **Which features influenced the model prediction, and how?**

---

# 2. ហេតុអ្វី Explainability សំខាន់ក្នុង PHM?

ក្នុង industrial PHM យើងមិនអាចទុកចិត្ត model ដោយសារ model មាន accuracy ខ្ពស់តែមួយមុខទេ។

ឧទាហរណ៍ model ប្រាប់៖

> "IGBT health is getting worse."

Engineer ចង់ដឹងថា model មើលឃើញអ្វី?

### Possibility A — Physical evidence

```text
Voltage Peak ↑
        ↓
Switching behavior changes
        ↓
Possible degradation-related signal
        ↓
Model predicts degradation
```

នេះអាចមានន័យសមហេតុផលជាង។

### Possibility B — Operating condition

```text
Temperature ↑
        ↓
Voltage/current changes
        ↓
Model predicts degradation
```

ប៉ុន្តែការផ្លាស់ប្តូរនោះប្រហែលមកពី **temperature condition** មិនមែន degradation ទេ។

### Possibility C — Sensor artifact

```text
Sensor drift
     ↓
Feature changes
     ↓
Model predicts degradation
```

Model អាចគិតថា equipment កំពុងខូច ទាំងដែល sensor មានបញ្ហា។

### Possibility D — Data leakage

```text
Future information
       ↓
Feature
       ↓
Model
       ↓
Very good prediction
```

Model អាចមាន performance ល្អខ្លាំង ប៉ុន្តែដោយសារ feature មាន information ដែលមិនគួរមាននៅពេល prediction។

**ដូច្នេះ Explainability អាចជួយឱ្យ engineer ស៊ើបអង្កេត model។**

---

# 3. Explainability ≠ Causality

ចំណុចនេះ **សំខាន់ណាស់** សម្រាប់ PHM។

បើ Explainability ប្រាប់ថា:

```text
Temperature
     ↓
important feature
```

វា **មិនមានន័យថា**

> Temperature caused the failure.

ទេ។

វាគ្រាន់តែមានន័យថា៖

> **The model relied strongly on Temperature when making its prediction.**

### ឧទាហរណ៍

```text
Temperature ──────┐
                  ↓
              Model
                  ↓
           Degradation ↑
```

យើងអាចនិយាយថា:

✅ Temperature was influential to the model prediction.

ប៉ុន្តែមិនគួរនិយាយថា:

❌ Temperature caused the degradation.

---

# 4. Explainability ក៏មិនអាច Validate HI បានទេ

ស្រដៀងនឹង Phase 6។

Suppose feature `Voltage Peak` មាន importance ខ្ពស់៖

```text
Voltage Peak
     ↓
High importance
```

នេះ **មិនមានន័យថា**

```text
Voltage Peak = Valid Health Indicator
```

ទេ។

ត្រូវការការត្រួតពិនិត្យផ្សេងទៀត៖

```text
Feature
   ↓
Physical meaning
   ↓
Consistent degradation relationship
   ↓
Monotonicity / sensitivity
   ↓
Operating-condition robustness
   ↓
Independent evidence
   ↓
Candidate HI validation
```

---

# 5. Common Explainability Methods

ក្នុង Machine Learning មាន methods ជាច្រើន។

### ① Feature Importance

សួរ៖

> Model ប្រើ feature ណាខ្លាំង?

ឧទាហរណ៍៖

```text
Feature              Importance

Voltage RMS             0.35
Current RMS             0.28
Temperature             0.20
Voltage Peak             0.12
Other                    0.05
```

វាជា **model-dependent importance**។

---

### ② Permutation Importance

Idea សាមញ្ញ៖

> បើខ្ញុំច្រឡំ/shuffle feature មួយ តើ model performance ធ្លាក់ប៉ុន្មាន?

ឧទាហរណ៍៖

```text
Original model
       ↓
MAE = 2.0

Shuffle Temperature
       ↓
MAE = 3.5
```

Performance ធ្លាក់ខ្លាំង → Temperature មានឥទ្ធិពលសំខាន់ចំពោះ model។

Flow:

```text
Original Dataset
      ↓
Train Model
      ↓
Measure Performance
      ↓
Shuffle ONE feature
      ↓
Measure Performance again
      ↓
Performance drop
      ↓
Feature importance
```

---

### ③ SHAP

**SHAP = SHapley Additive exPlanations**

វាព្យាយាមបង្ហាញថា feature នីមួយៗបានរួមចំណែកប៉ុន្មានទៅលើ prediction។

ឧទាហរណ៍៖

```text
Baseline prediction
       50
       │
       ├── Temperature     +8
       ├── Voltage RMS     +5
       ├── Current RMS     -3
       └── Voltage Peak    +2
                         ───
Final prediction          62
```

Conceptually:

$$
Prediction =
Baseline +
Contribution_1 +
Contribution_2 + ...
$$

SHAP អាចជួយឆ្លើយ៖

> **Why did this particular sample receive this prediction?**

---

# 6. Global vs Local Explainability

នេះក៏សំខាន់ដែរ។

### Global Explainability

មើល model ទាំងមូល៖

> "ជាទូទៅ model ពឹងផ្អែកលើ features អ្វី?"

```text
All samples
     ↓
Model
     ↓
Global feature importance
```

ឧទាហរណ៍៖

```text
Voltage RMS      ██████████
Temperature      ███████
Current RMS      █████
Voltage Peak     ███
```

---

### Local Explainability

មើល **sample មួយ**៖

> "ហេតុអ្វី model prediction សម្រាប់ observation នេះខ្ពស់?"

```text
Sample #1520

Temperature       +0.35
Voltage RMS       +0.22
Current RMS       -0.10
Voltage Peak      +0.05
                  ↓
            Prediction
```

ដូច្នេះ៖

```text
Global → What does the model generally use?

Local  → Why this particular prediction?
```

---

# 7. អនុវត្តទៅ IGBT Project របស់អ្នក

តាម Phase 8–11 ដែលយើងបានរៀន៖

```text
IGBT Dataset
     ↓
Feature Engineering
     ↓
Candidate HI
     ↓
Degradation analysis
     ↓
❌ No verified cohort-wide EoL
     ↓
❌ No defensible RUL target
     ↓
❌ No justified trained RUL model
```

ដូច្នេះយើង **មិនគួរ** ធ្វើ៖

```text
IGBT features
      ↓
RUL model
      ↓
SHAP
      ↓
"Voltage Peak causes RUL degradation"
```

ព្រោះ model ខាងក្នុងមិនទាន់មាន target ដែលអាចការពារបានតាម scientific basis។

---

# 8. ដូច្នេះ Phase 12 ប្រើ Synthetic Example

យើងអាចបង្កើត dataset តូចមួយដែលមាន target ត្រឹមត្រូវ៖

```text
Synthetic Dataset

Temperature
Voltage_RMS
Current_RMS
Voltage_Peak
       ↓
Synthetic ML Model
       ↓
Prediction
       ↓
Explainability
```

ឧទាហរណ៍៖

```text
Feature             Importance

Voltage_RMS             0.42
Temperature             0.27
Current_RMS             0.20
Voltage_Peak            0.11
```

នេះគ្រាន់តែបង្រៀន៖

> **How explainability methods work.**

វា **មិនមែន** ជា result របស់ IGBT PHM project ទេ។

---

# 9. អ្វីដែល Explainability អាចជួយបាន

| Explainability អាចជួយ                | Explainability មិនអាចបញ្ជាក់ដោយខ្លួនឯង |
| ------------------------------------ | -------------------------------------- |
| Model ពឹងលើ feature អ្វី             | Feature នោះជា causal factor            |
| Debug model                          | Failure mechanism                      |
| Detect suspicious feature dependence | Valid HI                               |
| Investigate sensor artifacts         | True RUL                               |
| Detect possible leakage clues        | Physical degradation                   |
| Understand individual predictions    | Model is automatically safe            |

ចំណុចសំខាន់៖

> **Explainability supports investigation; it does not replace validation.**

---

# 10. PHM Explainability Workflow

សម្រាប់ project របស់អ្នក អាចចងចាំជា៖

```text
              PHM Data
                  ↓
           Feature Engineering
                  ↓
          Valid Target / Outcome
                  ↓
             ML Model
                  ↓
              Prediction
                  ↓
          ┌───────┴────────┐
          ↓                ↓
     Global XAI         Local XAI
          ↓                ↓
 Feature importance    Why this prediction?
          └───────┬────────┘
                  ↓
        Engineering Investigation
                  ↓
      ┌───────────┼───────────┐
      ↓           ↓           ↓
 Physical      Sensor       Leakage
 evidence      artifact     check
      ↓           ↓           ↓
      └───────────┼───────────┘
                  ↓
          Engineering judgment
```

---

# 11. Connection ទៅ Phase 11

Phase 11 និង Phase 12 មានតួនាទីខុសគ្នា៖

### Phase 11 — Uncertainty

សួរ៖

> **How sure is the prediction?**

```text
Prediction = 20 hours
Uncertainty = ±3 hours
```

### Phase 12 — Explainability

សួរ៖

> **Why did the model make this prediction?**

```text
Temperature     → contribution
Voltage RMS     → contribution
Current RMS     → contribution
```

ដូច្នេះ៖

```text
Prediction
    │
    ├── Uncertainty
    │      ↓
    │   "How sure?"
    │
    └── Explainability
           ↓
        "Why?"
```

ទាំងពីរត្រូវបានប្រើជាមួយគ្នា ប៉ុន្តែមិនមែនជារឿងដូចគ្នាទេ។

---

## Key lesson សម្រាប់ Phase 12

ចំណុចដែលខ្ញុំណែនាំឱ្យអ្នកចងចាំសម្រាប់ presentation គឺ៖

> **Explainability helps engineers understand what a PHM model relies on, investigate suspicious predictions, and calibrate trust. However, feature importance is not causality, does not validate a Health Indicator, and cannot compensate for an invalid target or a poor model.**

សម្រាប់ **IGBT project របស់អ្នក**៖

```text
No verified EoL
      ↓
No defensible RUL target
      ↓
No justified RUL model
      ↓
No real IGBT RUL explainability result
      ↓
Use synthetic example
      ↓
Learn Feature Importance / Permutation Importance / SHAP
```

នេះជាការរក្សា **scientific integrity** របស់ project — យើងរៀន Explainability ដោយមិនបង្កើត claim ដែល dataset មិនអាចគាំទ្រ។
