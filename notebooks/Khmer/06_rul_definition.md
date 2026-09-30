# Phase 8 — Define RUL before creating labels

Phase 8 គឺជាដំណាក់កាល **សំខាន់ណាស់** មុនពេលយើងចាប់ផ្តើមធ្វើ **RUL prediction**។

គំនិតសំខាន់គឺ៖

> **មុននឹងបង្កើត RUL label យើងត្រូវកំណត់ឱ្យច្បាស់ថា “End of Life (EoL)” មានន័យថាអ្វី។**

---

## 1. RUL គឺជាអ្វី?

**RUL = Remaining Useful Life**

មានន័យថា៖

> រយៈពេល / ចំនួន cycles / accumulated dose ដែលនៅសល់ ចាប់ពី **current observation** រហូតដល់ **predefined End of Life (EoL)**។

Formula៖

$$
\mathrm{RUL}(t)=t_{\mathrm{EoL}}-t
$$

ឧទាហរណ៍៖

```text
Beginning of Life                         End of Life
      │                                        │
      ▼                                        ▼
      ●───────────────●───────────────●────────●
                      ↑
                 Current time
                      │
                      └──────── RUL ──────────→
```

បើ៖

* Current time = 80 hours
* EoL = 100 hours

នោះ៖

$$
RUL=100-80=20\text{ hours}
$$

---

# 2. EoL ត្រូវកំណត់ជាមុន

នេះជាចំណុចសំខាន់បំផុត។

**EoL មិនមែនគ្រាន់តែ “last data point” ទេ។**

ត្រូវមាន **physically meaningful failure criterion**។

ឧទាហរណ៍ conceptually៖

```text
Healthy
   ↓
Aging
   ↓
Degradation
   ↓
EoL criterion reached
   ↓
Failure / End of Life
```

EoL អាចត្រូវបានកំណត់ដោយ៖

* electrical performance limit
* thermal limit
* switching characteristic limit
* predefined failure criterion
* physical failure event
* experimentally documented end condition

ចំណុចសំខាន់៖ **EoL ត្រូវមានហេតុផលផ្នែករូបវិទ្យា (physical justification)**។

---

# 3. RUL មិនចាំបាច់ជា “Time”

Formula ខាងលើប្រើ time៖

$$
RUL=t_{EoL}-t
$$

ប៉ុន្តែសម្រាប់ប្រព័ន្ធផ្សេងៗ អាចប្រើ coordinate ផ្សេងបាន។

### Continuous operation

```text
RUL → hours
```

### Cycling system

```text
RUL → cycles
```

ឧទាហរណ៍៖

$$
RUL = N_{EoL}-N
$$

ដែល \(N\) = cycle count។

### Accelerated aging experiment

អាចប្រើ៖

```text
Time under stress
```

ឬ

```text
Cumulative thermal/electrical dose
```

ដូច្នេះ៖

> **RUL unit ត្រូវសមនឹង physical aging process។**

---

# 4. ហេតុអ្វី Calendar Time មិនស្មើ Useful Life?

នេះជាចំណុចដែលសំខាន់សម្រាប់ project របស់អ្នក។

ឧទាហរណ៍៖

Device A:

```text
8 hours/day × high electrical stress
```

Device B:

```text
8 hours/day × low electrical stress
```

ទោះបី calendar time ដូចគ្នា៖

```text
8 hours
```

ក៏ exposure/stress មិនដូចគ្នា។

ដូច្នេះ៖

```text
Calendar Time
      ≠
Useful Aging Exposure
```

សម្រាប់ PHM យើងចង់បាន coordinate ដែលមានន័យទាក់ទងនឹង **aging/degradation**។

---

# 5. BoL — Beginning of Life

RUL ក៏ត្រូវការចំណុចចាប់ផ្តើមដែលមានន័យ។

**BoL = Beginning of Life**

Conceptually៖

```text
BoL
 │
 ▼
Initial healthy state
 │
 ▼
Aging exposure
 │
 ▼
Current observation
 │
 ▼
EoL
```

ដូច្នេះ \(t\) គួរតែតំណាងឱ្យ **elapsed exposure** ពី BoL ដែលអាចការពារបានតាម evidence។

មិនមែនគ្រាន់តែយក timestamp ពី computer មកនិយាយថា៖

> “នេះគឺ aging time”

ដោយស្វ័យប្រវត្តិនោះទេ។

---

# 6. ចំណុចសំខាន់សម្រាប់ Dataset របស់អ្នក

នៅក្នុង Phase 7 យើងបានប្រើ៖

```text
timeEpoch
```

ជា **within-device recorded-time proxy**។

ប៉ុន្តែវាមិនត្រូវបានបញ្ជាក់ថាជា៖

```text
❌ Cycle count
❌ Thermal dose
❌ Electrical aging dose
❌ Verified degradation exposure
❌ EoL time
```

ដូច្នេះ Phase 8 យើងមិនអាចនិយាយថា៖

```text
RUL = last_time - current_time
```

បានទេ ប្រសិនបើយើងមិនដឹងថា **last_time គឺ EoL**។

---

# 7. Last Measurement ≠ EoL

នេះគឺជា **key concept** របស់ Phase 8។

ស្រមៃថា data របស់ device មាន៖

```text
Observation 1
Observation 2
Observation 3
...
Observation 100 ← last measurement
```

វាមិនមានន័យថា៖

```text
Observation 100 = Failure
```

ទេ។

វាអាចមានន័យថា៖

```text
Experiment stopped
        ↓
Data collection stopped
        ↓
Last observation
```

ប៉ុន្តែ device ប្រហែលជា **នៅដំណើរការ**។

---

# 8. Right-Censoring

នេះជាពាក្យសំខាន់មួយក្នុង PHM និង survival analysis។

បើ experiment ឈប់មុន device failure ហើយយើងដឹងថា device នៅ operational នៅពេលចុងក្រោយ៖

> **True EoL មិនត្រូវបាន observed។**

Data នោះគេហៅថា:

**Right-censored observation**

ឧទាហរណ៍៖

```text
BoL                                      Observation stops
 │                                              │
 ▼                                              ▼
 ●───────────────●───────────────●──────────────●
                                                ↑
                                           Still working
                                                │
                                                └── True EoL?
                                                     UNKNOWN
```

យើងដឹងថា៖

$$
t_{EoL} > t_{last}
$$

ប៉ុន្តែយើង **មិនដឹង exact \(t_{EoL}\)** ទេ។

ដូច្នេះ៖

$$
RUL(t_{last})
$$

ក៏ **unknown** ដែរ។

---

# 9. កុំធ្វើកំហុសនេះ ❌

Suppose:

```text
Last measurement = 100 hours
```

អ្នកអាចនឹងគិតថា៖

$$
t_{EoL}=100
$$

ហើយបង្កើត៖

$$
RUL=100-t
$$

**នេះខុស** ប្រសិនបើ 100 hours គ្រាន់តែជា last observation។

ត្រឹមត្រូវជាងគេគឺ៖

```text
Last observation
      ↓
Observation boundary
      ↓
Not necessarily EoL
```

---

# 10. Phase 8 មិនទាន់បង្កើត RUL Labels

នេះជាអ្វីដែល Phase 8 ចង់ឱ្យយើងធ្វើ៖

```text
              Phase 8
                 │
                 ▼
        Define RUL concept
                 │
                 ▼
       Identify possible BoL
                 │
                 ▼
       Define possible EoL
                 │
                 ▼
      Identify aging coordinate
                 │
                 ▼
     Determine what records support
                 │
                 ▼
      Can RUL be observed?
          /              \
        Yes               No
         │                 │
         ▼                 ▼
   RUL possible       Right-censored
```

**Phase 8 មិនធ្វើ៖**

```text
❌ Artificial EoL
❌ Fake RUL labels
❌ Assume last measurement = failure
❌ Train RUL model
```

---

# 11. Phase 8 vs Phase 7

| Phase                              | Main Question                                            |
| ---------------------------------- | -------------------------------------------------------- |
| **Phase 7 — Degradation Modeling** | Feature មាន trajectory យ៉ាងដូចម្តេចតាម recorded time?    |
| **Phase 8 — RUL Definition**       | តើយើងអាចកំណត់ EoL និង RUL ដោយមាន physical meaning បានទេ? |

ឬចងចាំជា៖

```text
Phase 7
"What changes over time?"
        ↓
Phase 8
"How do we define the remaining life?"
        ↓
Future RUL modeling
```

---

# 12. ហេតុអ្វី Phase 8 មុន RUL Prediction?

ព្រោះ Machine Learning model ត្រូវការ **target/label**។

ឧទាហរណ៍៖

```text
Input
  ↓
Voltage
Current
Temperature
Features
  ↓
ML Model
  ↓
RUL
```

ប៉ុន្តែបើ RUL label ខុស៖

```text
Wrong EoL
    ↓
Wrong RUL labels
    ↓
Wrong training target
    ↓
Wrong model
    ↓
Misleading prediction
```

ដូច្នេះ៖

> **Good RUL model cannot compensate for an invalid RUL definition.**

---

# 13. Flow ដែលគួរចងចាំ

```text
Raw measurements
       ↓
Feature Engineering
       ↓
Candidate Health Indicator
       ↓
Degradation Modeling
       ↓
       ┌──────────────────────┐
       │ Define BoL           │
       │ Define EoL           │
       │ Define aging clock   │
       │ Check failure data   │
       └──────────────────────┘
                    ↓
             Can EoL be observed?
               /           \
             Yes            No
              ↓             ↓
        RUL may be       Right-censored
        calculable       observation
              │
              ↓
       RUL Prediction
```

## ⭐ ចំណុចដែលអ្នកគួរចាំសម្រាប់ PHM Presentation

**Phase 8 = “Define before predicting.”**

មានន័យថា មុននឹងនិយាយថា៖

> “This model predicts RUL.”

ត្រូវអាចឆ្លើយបានជាមុន៖

1. **What is BoL?**
2. **What is EoL?**
3. **What is the physical failure criterion?**
4. **What is the aging coordinate — time, cycles, or dose?**
5. **Was EoL actually observed?**
6. **If not, is the observation right-censored?**

សម្រាប់ **NASA IGBT dataset project របស់អ្នក** Phase 8 គឺមិនមែនបង្ខំឱ្យយើងបង្កើត RUL ទេ។ វាគឺជាការត្រួតពិនិត្យថា **dataset មាន evidence គ្រប់គ្រាន់សម្រាប់បង្កើត physically defensible RUL labels ឬអត់**។
