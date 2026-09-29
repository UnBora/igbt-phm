បាន។ ខាងក្រោមនេះជាការពន្យល់ជា **ភាសាខ្មែរ** ដោយខ្ញុំនឹងរក្សា **English technical keywords** ដូចជា `PHM`, `RUL`, `Dataset`, `Degradation`, `Health Indicator`, `EOL`, `MAT files`, `DataFrame` ដើម្បីឱ្យងាយស្របជាមួយការសិក្សារបស់អ្នក។

# NASA IGBT PHM Learning Project

គម្រោងនេះគឺជា **hands-on, progressive study** ដែលមានន័យថា យើងរៀន PHM តាមរយៈការអនុវត្តជាក់ស្តែង និងធ្វើជាដំណាក់កាលៗ។

យើងប្រើ **NASA IGBT Accelerated Aging Dataset** ដើម្បីសិក្សា PHM។

គោលដៅដំបូង **មិនទាន់មែនជា RUL prediction** ទេ។ យើងត្រូវយល់ជាមុនថា៖

> **Experiment → Measurement → Data → Degradation → Health → RUL**

មានន័យថា យើងត្រូវយល់ពី **ការពិសោធន៍ និង measurement** ជាមុនសិន មុននឹងធ្វើ `Degradation Analysis` ឬ `RUL Prediction`។

---

# Phase 1 — Dataset Understanding

### Dataset គឺជាអ្វី?

`Dataset` គឺជាទិន្នន័យដែល NASA បានប្រមូលពីការធ្វើតេស្ត **IGBT (Insulated Gate Bipolar Transistor)**។

ទិន្នន័យដែលបាន extract រួច ស្ថិតនៅ៖

```text
data/raw/IGBTAgingData_04022009/
```

មានន័យថា៖

* `data/` → folder សម្រាប់ data
* `raw/` → original/unprocessed data
* `IGBTAgingData_04022009/` → folder ដែលមាន dataset របស់ IGBT Aging

Original ZIP file មិនត្រូវបានរកឃើញនៅក្នុង `data/raw/` ទេ។ ប៉ុន្តែ dataset ត្រូវបាន **extract** រួចហើយ។

---

## Step 1 — Create Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

មានន័យថា យើងបង្កើត **Python Virtual Environment** មួយសម្រាប់ project នេះ។

### `.venv`

វាជា environment ដាច់ដោយឡែកសម្រាប់ Python packages របស់ project។

ឧទាហរណ៍៖

```text
NASA IGBT PHM Project
│
├── .venv/
├── data/
├── notebooks/
├── src/
└── requirements.txt
```

`requirements.txt` មាន packages ដែល project ត្រូវការ ដូចជា `pandas`, `numpy`, `matplotlib`, `scipy` ជាដើម។

---

# Step 2 — Dataset Exploration

បើក៖

```text
notebooks/01_data_exploration.ipynb
```

ក្នុង **VS Code** ហើយជ្រើស `.venv` ជា Python Interpreter/Kernel។

បន្ទាប់មក run cells **តាមលំដាប់**។

គោលបំណងរបស់ Phase 1 គឺ៖

> **Understand the dataset before analyzing it.**

យើងត្រូវពិនិត្យ៖

* Dataset មាន files អ្វីខ្លះ?
* មាន experiment ប៉ុន្មាន?
* មាន measurement អ្វីខ្លះ?
* `MAT file` មាន structure ដូចម្តេច?
* Timestamp មានអ្វីខ្លះ?
* Measurement មាន missing values ឬទេ?
* Measurement ណាខ្លះអាចប្រើបាន?

---

# Important: Dataset មាន Limitations

នេះជាចំណុច **សំខាន់ខ្លាំងសម្រាប់ PHM**។

Documentation របស់ dataset រាយការណ៍ថា មានបញ្ហាមួយចំនួន៖

### 1. Missing transient measurements

មាន `Transient measurements` មួយចំនួនដែលបាត់។

មានន័យថា យើងមិនមាន transient data ពេញលេញសម្រាប់គ្រប់ measurement ទេ។

---

### 2. Collector-current drift

`Collector current` មាន **drift**។

`Drift` មានន័យថា signal ផ្លាស់ប្តូរបន្តិចម្តងៗ ដោយមិនប្រាកដថាការផ្លាស់ប្តូរនោះកើតឡើងពី physical degradation ពិតប្រាកដទេ។

ឧទាហរណ៍៖

```text
Observed change
      ↓
Is it degradation?
      ↓
Maybe yes
      ↓
OR
      ↓
Measurement drift
```

ដូច្នេះ យើងមិនអាចឃើញ signal ផ្លាស់ប្តូរ ហើយសន្និដ្ឋានភ្លាមថា **IGBT is degrading** បានទេ។

---

### 3. Improperly scaled steady-state measurements

`Steady-state measurements` មួយចំនួនមានបញ្ហា **scaling**។

មានន័យថា តម្លៃដែលយើងឃើញក្នុង data អាចមិនត្រូវបាន scale តាម unit/scale ដែលយើងរំពឹងទុក។

ដូច្នេះ៖

> **Do not assume every numerical value has a valid physical unit.**

នេះសំខាន់ណាស់។

---

# Signal fields ≠ Failure Labels

Notebook នឹងព្រមានថា យើងមិនត្រូវសន្មតថា `signal fields` ជា `failure labels` ទេ។

ឧទាហរណ៍ បើយើងឃើញ៖

```text
Current = 10
Current = 11
Current = 12
Current = 15
```

យើងមិនអាចនិយាយភ្លាមថា៖

> "IGBT is failing."

ទេ។

យើងត្រូវសួរមុនថា៖

* តើ change នេះមកពី degradation?
* Temperature បានផ្លាស់ប្តូរឬទេ?
* Supply condition បានផ្លាស់ប្តូរឬទេ?
* Measurement drift ឬទេ?
* Scale problem ឬទេ?

---

# Phase 2 — Data Loading

បន្ទាប់ពីយល់ពី Phase 1 រួច ចូល៖

```text
notebooks/02_data_loading.ipynb
```

Phase នេះចាប់ផ្តើម **load actual data**។

វានឹង load `steady-state records` ពី **10 MAT files** ដែលស្ថិតក្នុង folder៖

```text
Device 2–5 square-gate aging folder
```

---

## DataFrame គឺជាអ្វី?

នៅក្នុង Python យើងនឹងប្រើ `pandas DataFrame` ដើម្បីតំណាងឱ្យ data។

គំនិតប្រហែល៖

| Time | Current | Voltage | Temperature | Source |
| ---- | ------: | ------: | ----------: | ------ |
| t1   |     ... |     ... |         ... | file1  |
| t2   |     ... |     ... |         ... | file1  |
| t3   |     ... |     ... |         ... | file2  |

DataFrame គឺដូចជា **Excel table** ប៉ុន្តែយើងអាច process វាដោយ Python។

---

## `check` និង Source Identifier

Project នឹងរក្សា `check` និង file segments ផ្សេងៗ ហើយបន្ថែម `source identifiers`។

មានន័យថា យើងចង់ដឹងថា៖

> **This observation came from which original file?**

ឧទាហរណ៍៖

```text
Observation
   ↓
file_01.mat
```

ឬ

```text
Observation
   ↓
file_07.mat
```

វាសំខាន់សម្រាប់ PHM ព្រោះយើងមិនគួរលាយ data ពី source ផ្សេងៗគ្នាដោយមិនដឹងប្រភពទេ។

---

# Phase 2 នឹងពិនិត្យអ្វីខ្លះ?

Notebook នឹងបង្រៀនអ្នកពិនិត្យ៖

### 1. DataFrame shape

ឧទាហរណ៍៖

```text
(5000, 20)
```

មានន័យថា៖

* 5000 rows
* 20 columns

---

### 2. Data types

ឧទាហរណ៍៖

```text
float
integer
string
datetime
```

យើងត្រូវដឹងថា column នីមួយៗមាន data type អ្វី។

---

### 3. Missingness

រកមើល៖

```text
NaN
Missing values
Empty values
```

ដើម្បីដឹងថា data មានចន្លោះបាត់ឬអត់។

---

### 4. Numeric descriptions

ឧទាហរណ៍៖

```text
mean
std
min
max
median
```

ដើម្បីយល់ពី distribution របស់ data។

---

### 5. Timestamp intervals

យើងពិនិត្យថា data ត្រូវបាន recorded នៅពេលណា និងមាន time interval ដូចម្តេច។

---

# Output របស់ Phase 2

Notebook នឹងបង្កើត៖

```text
data/processed/aging_steady_state_observations.csv
```

មានន័យថា៖

```text
Raw MAT files
      ↓
Data Loading
      ↓
Processed CSV
```

**សំខាន់:** Original MAT files **មិនត្រូវបានកែប្រែទេ**។

CSV នេះក៏មិនមែនជា copy ដែលរក្សាទុក data ទាំងអស់ 100% ដែរ។

វា **មិនមាន separate transient waveforms** ទេ។

---

# Phase 3 — Exploratory Data Analysis (EDA)

បន្ទាប់ពី Phase 2 រួច ចូល៖

```text
notebooks/03_exploratory_data_analysis.ipynb
```

`EDA = Exploratory Data Analysis`

មានន័យថា៖

> **Explore the data to understand what is happening.**

មិនទាន់ជា machine learning ទេ។

---

## Phase 3 នឹងធ្វើអ្វី?

### 1. Plot selected signals over time

យើង plot signal តាមពេលវេលា៖

```text
Signal
  │
  │       /
  │     /
  │   /
  │__/
  └────────── Time
```

ដើម្បីសង្កេត៖

> តើ signal មានការផ្លាស់ប្តូរតាមពេលវេលាដែរឬទេ?

---

### 2. Do not connect file segments

ចំណុចនេះសំខាន់។

យើងមិនគួរភ្ជាប់ data ពី file មួយទៅ file មួយ ដូចជាវាជា continuous experiment តែមួយទេ ប្រសិនបើ data structure មិនបញ្ជាក់បែបនោះ។

---

### 3. Populated-channel distributions

ពិនិត្យថា channel ណាខ្លះមាន data ច្រើន និង channel ណាខ្លះមាន data តិច។

---

### 4. Compare values by source file

ប្រៀបធៀប measurement របស់៖

```text
file 1
file 2
file 3
...
file 10
```

ដើម្បីមើលថា file នីមួយៗមានលក្ខណៈដូចម្តេច។

---

### 5. Correlation

យើងអាចមើល `pairwise correlations` រវាង signals។

ឧទាហរណ៍៖

```text
Temperature ↔ Current
Voltage     ↔ Current
Temperature ↔ Voltage
```

ប៉ុន្តែ៖

> **Correlation ≠ Causation**

មាន correlation មិនមានន័យថា signal មួយជាមូលហេតុនៃ signal មួយទៀតទេ។

---

# PHM Question ក្នុងគ្រប់ Plot

Project នេះមិនចង់ឱ្យអ្នកគ្រាន់តែ plot graph ហើយមើលវាទេ។

រាល់ plot គួរតែមាន **PHM question**។

ឧទាហរណ៍៖

> "Does this signal show a consistent trend that could potentially indicate degradation?"

ប៉ុន្តែយើងត្រូវប្រយ័ត្ន ព្រោះ trend អាចបណ្តាលមកពី៖

* controlled temperature changes
* supply changes
* measurement drift
* scaling problems

មិនមែន degradation ទាំងអស់ទេ។

---

# Phase 3 មិនទាន់ធ្វើអ្វីខ្លះ?

នេះជាចំណុចសំខាន់បំផុត។

Phase 3 **មិនទាន់**៖

❌ Clean observations
❌ Select final Health Indicator
❌ Create RUL targets
❌ Train machine-learning models
❌ Predict RUL

ហេតុផលគឺ៖

> **First understand the data. Then decide what processing/modeling is scientifically justified.**

---

# Hold Off on Existing RUL Prototype

មាន RUL prototype ចាស់នៅ៖

```text
src/rul.py
```

និង៖

```text
notebooks/05_rul_baseline.ipynb
```

ប៉ុន្តែ **កុំប្រើវាឥឡូវនេះ**។

---

# ហេតុអ្វី RUL Prototype មិនទាន់គួរប្រើ?

Prototype នោះកំណត់៖

```text
RUL = Last recorded time - Current time
```

ឬគំនិតប្រហែល៖

> "Time remaining until the last observation."

បញ្ហាគឺ៖

**Last recorded observation ≠ Physical End of Life (EOL)**

---

## ឧទាហរណ៍

បើ experiment ឈប់នៅ៖

```text
Day 100
```

Prototype អាចនិយាយថា៖

```text
RUL at Day 50 = 50 days
```

ប៉ុន្តែយើងមិនដឹងថា៖

> តើ IGBT ពិតជាបរាជ័យនៅ Day 100 មែនទេ?

ប្រហែល experiment គ្រាន់តែ **ឈប់ recording**។

ដូច្នេះ៖

```text
Last observation
       ≠
Failure
       ≠
EOL
```

ហេតុនេះ RUL ដែលបានពី prototype គឺគ្រាន់តែជា **proxy target** មិនមែនជា physical RUL ដែលបានបញ្ជាក់ទេ។

---

# EOL = End of Life

មុននឹងធ្វើ RUL prediction យើងត្រូវកំណត់៖

> **What exactly means "End of Life" for this IGBT?**

ឧទាហរណ៍ អាចជាលក្ខខណ្ឌដែលមាន physical failure ឬ performance degradation ដល់ threshold មួយ។

ប៉ុន្តែសម្រាប់ dataset នេះ យើងត្រូវសិក្សា documentation និង device events ជាមុនសិន។

---

# Censoring

`Censoring` មានន័យថា យើងមាន observation ត្រឹមចំណុចណាមួយ ប៉ុន្តែមិនបានឃើញ actual failure។

ឧទាហរណ៍៖

```text
Healthy ─────── Aging ─────── ? 
                              ↑
                         experiment stopped
```

យើងមិនអាចនិយាយថា `? = Failure` បានទេ។

នេះជាមូលហេតុដែល RUL modeling ត្រូវរង់ចាំ។

---

# Final Project Workflow

គម្រោងនេះចង់ឱ្យអ្នករៀនតាម flow នេះ៖

```text
NASA IGBT Dataset
       ↓
Phase 1
Dataset Understanding
       ↓
Understand Experiment
       ↓
Understand Measurements
       ↓
Understand Limitations
       ↓
Phase 2
Data Loading
       ↓
MAT Files → DataFrame → CSV
       ↓
Phase 3
Exploratory Data Analysis
       ↓
Understand Signals
       ↓
Understand Trends
       ↓
Understand Correlations
       ↓
Identify Possible Degradation Evidence
       ↓
Define EOL
       ↓
Define Health Indicator
       ↓
Create Defensible RUL Target
       ↓
Modeling
       ↓
RUL Prediction
       ↓
Evaluation
```

## គំនិតសំខាន់ដែលអ្នកគួរចងចាំ

**PHM មិនមែនជា៖**

> Data → Machine Learning → RUL

ប៉ុណ្ណោះទេ។

សម្រាប់ project នេះ យើងកំពុងរៀនវិធីដែលត្រឹមត្រូវជាងនេះ៖

> **Experiment → Measurement → Data Understanding → EDA → Degradation Evidence → Health Indicator → EOL Definition → RUL Target → Model → Evaluation**

ហើយសម្រាប់ពេលនេះ **គោលដៅរបស់អ្នកគឺ Phase 1 → Phase 2 → Phase 3**។ កុំប្រញាប់ទៅ `RUL prediction` មុនពេលយល់ថា data នេះមានន័យអ្វី និង limitations របស់វាជាអ្វី។
