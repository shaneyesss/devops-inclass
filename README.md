# DevOps Homework: Continuous Integration with GitHub Actions

**Master of Science in Health Informatics – Application Development**
**UT Southwestern Medical Center**

---

## Table of Contents

1. [Learning Objectives](#1-learning-objectives)
2. [Background: What Is Continuous Integration?](#2-background-what-is-continuous-integration)
3. [GitHub Actions: CI in Practice](#3-github-actions-ci-in-practice)
4. [Repository Overview](#4-repository-overview)
5. [The Clinical Calculators](#5-the-clinical-calculators)
6. [Your Assignment](#6-your-assignment)
7. [Step-by-Step Instructions](#7-step-by-step-instructions)
8. [Running Tests Locally](#8-running-tests-locally)
9. [Scoring Rubric](#9-scoring-rubric)
10. [Appendix: Clinical Reference](#10-appendix-clinical-reference)

---

## 1. Learning Objectives

By completing this assignment you will be able to:

- Explain the concept of **Continuous Integration (CI)** and why it matters in
  software development.
- Read and interpret a **GitHub Actions workflow** file (`.github/workflows/ci.yml`).
- Write Python functions that satisfy a pre-existing test suite.
- Experience first-hand how a CI pipeline enforces code quality by blocking
  a push when tests fail.

---

## 2. Background: What Is Continuous Integration?

### The Problem CI Solves

Imagine a team of five developers all working on the same codebase.
Each person writes code in isolation for two weeks and then everyone tries to
merge their work together.  The result is often called *integration hell*:
dozens of conflicting changes, broken tests, and hours of debugging.

**Continuous Integration (CI)** is a DevOps practice that prevents this by
requiring every developer to integrate (merge) their changes back into the
shared codebase *frequently* — often several times per day.  Each integration
is verified automatically by running a build and a suite of automated tests.

### The Core Principles of CI

| Principle | What it means |
|-----------|---------------|
| **Commit early, commit often** | Small, frequent commits are easier to review and less likely to break things. |
| **Build on every commit** | An automated system builds and tests the code every time someone pushes. |
| **Fix broken builds immediately** | A failing CI pipeline is treated as the highest priority. Everyone stops until it is fixed. |
| **Tests are the safety net** | Without automated tests, CI is just automation of "did it compile?". Good tests catch real bugs. |
| **Fail fast** | If something is broken, find out in minutes, not days. |

### CI in Healthcare Software

Healthcare applications are safety-critical.  A bug in a clinical decision
support tool could contribute to patient harm.  CI helps teams:

- Catch regressions before they reach production.
- Enforce that new features do not silently break existing behaviour.
- Give reviewers confidence that a pull request does not introduce bugs.
- Maintain an auditable record of every change and every test run.

---

## 3. GitHub Actions: CI in Practice

### What Are GitHub Actions?

**GitHub Actions** is GitHub's built-in CI/CD (Continuous Integration /
Continuous Delivery) platform.  It lets you automate tasks — such as running
tests, linting code, or deploying an application — by writing *workflows* in
YAML files stored in the `.github/workflows/` directory of your repository.

### Anatomy of a Workflow File

Open `.github/workflows/ci.yml` and read through it.  Here is what each
section means:

```yaml
name: CI – Run All Tests          # Human-readable name shown in GitHub UI
```

```yaml
on:                               # Trigger(s) for the workflow
  push:
    branches: [ "main" ]          # Run when code is pushed to main
  pull_request:
    branches: [ "main" ]          # Run when a PR targets main
```

```yaml
jobs:                             # One or more jobs to execute
  test:
    runs-on: ubuntu-latest        # Fresh Ubuntu virtual machine
    steps:
      - uses: actions/checkout@v4           # Step 1: clone the repo
      - uses: actions/setup-python@v5       # Step 2: install Python
        with:
          python-version: "3.11"
      - name: Install dependencies          # Step 3: pip install
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests with pytest         # Step 4: run the tests
        run: |
          pytest test_calculators.py -v --tb=short
```

### How CI Enforces Code Quality

When you push a commit to `main`:

1. GitHub automatically starts a new workflow *run*.
2. A fresh virtual machine is spun up.
3. Your code is checked out, dependencies are installed, and the test suite is
   run.
4. If **all tests pass** → the commit is marked ✅ and the push succeeds.
5. If **any test fails** → the commit is marked ❌.  With *branch protection
   rules* enabled (see §7.5), the push would be blocked entirely.

You can see every workflow run under the **Actions** tab of your repository.

---

## 4. Repository Overview

```
devops-homework/
├── calculators.py          ← Scoring functions (some need implementation!)
├── app.py                  ← Flask REST API (pre-built, no changes needed)
├── test_calculators.py     ← Test suite (pre-built, no changes needed)
├── requirements.txt        ← Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml          ← GitHub Actions CI workflow
└── README.md               ← This file
```

### `calculators.py`

Contains five clinical scoring functions.  **Three are fully implemented**
(PERC, CHA₂DS₂-VASc, ASCVD).  **Two have stubs that raise**
`NotImplementedError` — those are yours to implement.

### `test_calculators.py`

Contains automated tests for **all five** functions.  Tests for the
pre-implemented functions pass immediately.  Tests for the student functions
will fail until you implement them correctly.  Do **not** modify this file.

### `app.py`

A Flask REST API that exposes each calculator as a `POST` endpoint.  You do
not need to modify this file.  It is provided so you can interact with your
calculators via HTTP if you wish.

---

## 5. The Clinical Calculators

### Pre-Implemented (provided for you)

#### PERC – PE Rule-Out Criteria
Used to rule out pulmonary embolism in patients with **low pretest
probability**.  Eight binary criteria; if all are absent the patient is
"PERC negative" and PE can be excluded without further testing.

#### CHA₂DS₂-VASc Score
Estimates annual **stroke risk in non-valvular atrial fibrillation**.
Guides anticoagulation therapy decisions.  Each risk factor contributes 1
or 2 points; scores ≥ 2 generally warrant anticoagulation.

#### 10-Year ASCVD Risk (Pooled Cohort Equations)
Estimates the 10-year probability of a first **atherosclerotic
cardiovascular event** (MI or stroke) using the 2013 ACC/AHA Pooled Cohort
Equations.  Guides statin therapy initiation.

---

### Student-Implemented (you write these)

#### HEART Score
Risk-stratifies emergency department patients presenting with **chest pain**
for major adverse cardiac events (MACE: MI, PCI, CABG, or death within 6
weeks).  Five components, each scored 0–2; total score 0–10.

| Score | Risk Level | Approx. MACE Rate | Management |
|-------|------------|-------------------|------------|
| 0–3   | Low        | ~1.7 %            | Consider early discharge |
| 4–6   | Moderate   | ~12 %             | Observe + serial troponins |
| 7–10  | High       | ~65 %             | Early invasive strategy |

#### PECARN Pediatric Head Injury
Identifies children at **very low risk** of clinically important traumatic
brain injury (ciTBI) for whom CT can be safely avoided, reducing unnecessary
radiation exposure.  The rule differs for children under vs. over 24 months.

---

## 6. Your Assignment

### What You Need to Do

Implement **two functions** in `calculators.py`:

1. **`calculate_heart_score(history, ecg, age_score, risk_factors, troponin)`**
2. **`calculate_pecarn(age_months, gcs, altered_mental_status, ...)`**

Both functions have detailed docstrings with step-by-step instructions.  Read
the `TODO for Students` section inside each docstring carefully.

### What You Must NOT Do

- Do **not** modify `test_calculators.py`.
- Do **not** modify `app.py`.
- Do **not** modify `.github/workflows/ci.yml`.
- Do **not** change the function signatures in `calculators.py`.

---

## 7. Step-by-Step Instructions

### 7.1 Fork and Clone the Repository

1. Click **Fork** in the top-right corner of the GitHub repository page to
   create your own copy.
2.
   1. If running in Codespaces, simply create a new Codespace on Main and then skip to **Step 7.3**.
   2. If running locally, clone your fork and then continue to **Step 7.2**:

   ```bash
   git clone https://github.com/<your-username>/devops-homework.git
   cd devops-homework
   ```

### 7.2 (Only if running locally) Create a Virtual Environment and Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 7.3 Verify the Starting State (Tests Should Fail)

Run the test suite before writing any code:

```bash
pytest test_calculators.py -v
```

You should see several test failures

```
PASSED  test_calculators.py::TestPERC::test_perc_negative_all_low_risk
PASSED  test_calculators.py::TestCHADSVASc::test_score_zero_young_male_no_risk_factors
PASSED  test_calculators.py::TestASCVD::test_white_male_low_risk
...
FAILED  test_calculators.py::TestHEARTScore::test_all_zeros_gives_score_zero
FAILED  test_calculators.py::TestPECARN::test_under2_high_risk_low_gcs
...
```

The three pre-implemented calculators pass; the two student functions fail
with `NotImplementedError`.  **This is expected.**

### 7.4 Implement the Two Functions

Open `calculators.py` and find:

- `calculate_heart_score()` (search for `TODO: Students`)
- `calculate_pecarn()` (search for `TODO: Students`)

Read the docstring for each function — it describes **exactly** what the
function must do, including the decision rules, validation requirements,
and the structure of the return value.

**Tips:**

- Start with `calculate_heart_score()` — it is simpler.
- Use the `TODO for Students` section inside each docstring as your guide.
- After each function, run `pytest` to see how many tests now pass.
- Make sure to handle `ValueError` for invalid inputs as described.

### 7.5 (Optional) Enable Branch Protection

To experience how CI *blocks* a bad push, enable branch protection on your
fork:

1. Go to your repository on GitHub → **Settings** → **Branches**.
2. Click **Add branch ruleset**.
3. Set the target branch to `main`.
4. Enable **Require status checks to pass before merging**.
5. Search for and add the status check named **"Run pytest test suite"**.
6. Save the ruleset.

Now if you try to push code that fails the tests, GitHub will reject the push.

### 7.6 Run Tests Until All Pass

Iterate on your implementation until all tests pass:

```bash
pytest test_calculators.py -v
```

Expected final output (all green):

```
PASSED  test_calculators.py::TestPERC::...           (10 tests)
PASSED  test_calculators.py::TestCHADSVASc::...      (10 tests)
PASSED  test_calculators.py::TestASCVD::...          ( 9 tests)
PASSED  test_calculators.py::TestHEARTScore::...     (11 tests)
PASSED  test_calculators.py::TestPECARN::...         (19 tests)

59 passed in X.XXs
```

### 7.7 Commit and Push to Main

```bash
git add calculators.py
git commit -m "Implement HEART score and PECARN calculators"
git push origin main
```

### 7.8 Watch the CI Pipeline Run

1. Navigate to your repository on GitHub.
2. Click the **Actions** tab.
3. You should see a workflow run triggered by your push.
4. Click on the run to expand it, then click on the **"Run pytest test suite"**
   job to see the live log output.
5. All 59 tests should pass and the workflow status should show ✅.

---

## 8. Running Tests Locally (Optional)

```bash
# Run all tests with verbose output
pytest test_calculators.py -v

# Run only HEART score tests
pytest test_calculators.py::TestHEARTScore -v

# Run only PECARN tests
pytest test_calculators.py::TestPECARN -v

# Stop after first failure
pytest test_calculators.py -x

# Show full traceback on failures
pytest test_calculators.py -v --tb=long
```

### Running the Flask App

```bash
python app.py
```

Then open the application in a browser to see it function.

---


### Submission

Submit via D2L

1. A link to your forked GitHub repository (ensure it is **public** or the
   instructor has been added as a collaborator).
2. A screenshot of the **GitHub Actions workflow run** showing all tests
   passing (the green ✅).

---

## 10. Appendix: Clinical Reference

### HEART Score – Component Definitions

| Component | 0 | 1 | 2 |
|-----------|---|---|---|
| **History** | Slightly suspicious | Moderately suspicious | Highly suspicious |
| **ECG** | Normal | Non-specific repolarisation disturbance | Significant ST deviation |
| **Age** | < 45 years | 45–64 years | ≥ 65 years |
| **Risk Factors** | No known risk factors | 1–2 risk factors or obesity (BMI > 30) | ≥ 3 risk factors, diabetes, or known atherosclerotic disease |
| **Troponin** | ≤ normal limit | 1–3 × normal limit | > 3 × normal limit |

Risk factors include: hypertension, hypercholesterolaemia, diabetes mellitus,
obesity (BMI > 30), current or recent smoking (< 90 days), positive family
history of CAD, or known atherosclerotic disease (prior PCI/CABG, stroke, PAD).

### PECARN Decision Rule – Summary

**Age < 24 months**

```
HIGH RISK (CT recommended) if ANY of:
  • GCS < 15
  • Palpable skull fracture
  • Altered mental status

INTERMEDIATE RISK if ANY of:
  • Loss of consciousness
  • Non-frontal scalp haematoma
  • Severe mechanism of injury *
  • Vomiting

LOW RISK: none of the above
```

**Age ≥ 24 months**

```
HIGH RISK (CT recommended) if ANY of:
  • GCS < 15
  • Signs of basilar skull fracture **
  • Altered mental status

INTERMEDIATE RISK if ANY of:
  • Loss of consciousness
  • Vomiting
  • Severe mechanism of injury *
  • Severe headache

LOW RISK: none of the above
```

\* Severe mechanism: fall > 3 ft (< 2 yr) or > 5 ft (≥ 2 yr); MVA with
ejection, rollover, or fatality; pedestrian/cyclist struck by vehicle; head
struck by high-impact object.

\*\* Signs of basilar skull fracture: haemotympanum, 'raccoon eyes',
retroauricular bruising (Battle's sign), CSF otorrhoea/rhinorrhoea.

---

*Clinical calculators in this repository are for **educational purposes only**
and must not be used for actual clinical decision-making.*
