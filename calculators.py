"""
Clinical Risk Score Calculators
================================

A collection of functions for calculating widely used clinical risk scores
used in evidence-based medicine. These calculators are intended for
educational purposes.

Pre-implemented calculators:
    - calculate_perc()      : PE Rule-Out Criteria
    - calculate_chads_vasc(): CHA₂DS₂-VASc Score (AFib stroke risk)
    - calculate_ascvd_risk(): 10-Year ASCVD Risk (Pooled Cohort Equations)

Student TODO - implement these two calculators:
    - calculate_heart_score(): HEART Score for chest pain risk stratification
    - calculate_pecarn()      : PECARN Pediatric Head Injury Decision Rule
"""

import math


# =============================================================================
# PERC - Pulmonary Embolism Rule-Out Criteria  (pre-implemented)
# =============================================================================

def calculate_perc(age, heart_rate, o2_sat, hemoptysis, estrogen_use,
                   prior_dvt_pe, unilateral_leg_swelling, surgery_trauma_4wks):
    """
    Calculate the Pulmonary Embolism Rule-Out Criteria (PERC) score.

    The PERC rule is used to rule out PE in patients who already have a
    *low* pretest probability. If ALL eight criteria are absent (score = 0)
    the diagnosis of PE can be excluded without further testing. Any positive
    criterion indicates that further evaluation is needed.

    Parameters
    ----------
    age : int
        Patient age in years.
    heart_rate : int
        Heart rate in beats per minute.
    o2_sat : float
        Oxygen saturation as a percentage (e.g. 95 for 95 %).
    hemoptysis : bool
        True if patient has haemoptysis.
    estrogen_use : bool
        True if patient uses exogenous oestrogen (OCP, HRT, etc.).
    prior_dvt_pe : bool
        True if patient has a prior history of DVT or PE.
    unilateral_leg_swelling : bool
        True if patient has unilateral leg swelling.
    surgery_trauma_4wks : bool
        True if patient had surgery or trauma requiring hospitalisation
        within the previous 4 weeks.

    Returns
    -------
    dict
        ``score``         - int  : number of positive criteria (0-8).
        ``perc_negative`` - bool : True when score == 0 (PE ruled out).
        ``interpretation``- str  : plain-language clinical interpretation.
    """
    criteria = [
        age >= 50,
        heart_rate >= 100,
        o2_sat < 95,
        bool(hemoptysis),
        bool(estrogen_use),
        bool(prior_dvt_pe),
        bool(unilateral_leg_swelling),
        bool(surgery_trauma_4wks),
    ]
    score = sum(criteria)
    perc_negative = score == 0

    if perc_negative:
        interpretation = (
            "PERC Negative: Low probability of PE. "
            "No further workup needed for PE based on PERC criteria."
        )
    else:
        interpretation = (
            "PERC Positive: Cannot rule out PE. "
            "Further evaluation (D-dimer or CT pulmonary angiography) is indicated."
        )

    return {
        "score": score,
        "perc_negative": perc_negative,
        "interpretation": interpretation,
    }


# =============================================================================
# CHA₂DS₂-VASc - Atrial Fibrillation Stroke Risk  (pre-implemented)
# =============================================================================

def calculate_chads_vasc(chf, hypertension, age, diabetes, stroke_tia,
                          vascular_disease, sex):
    """
    Calculate the CHA₂DS₂-VASc score for stroke risk in atrial fibrillation.

    This score guides anticoagulation decisions in patients with non-valvular
    atrial fibrillation. Higher scores correspond to greater annual stroke risk.

    Scoring
    -------
    C - Congestive heart failure (or LVEF < 40 %)        : +1
    H - Hypertension (treated or untreated)              : +1
    A₂- Age ≥ 75                                         : +2
    D - Diabetes mellitus                                : +1
    S₂- Prior stroke, TIA, or thromboembolism            : +2
    V - Vascular disease (prior MI, PAD, aortic plaque)  : +1
    A - Age 65–74                                        : +1
    Sc- Female sex                                       : +1

    Parameters
    ----------
    chf : bool
        Congestive heart failure or LVEF < 40 %.
    hypertension : bool
        Hypertension (treated or untreated).
    age : int
        Patient age in years.
    diabetes : bool
        Diabetes mellitus.
    stroke_tia : bool
        Prior stroke, TIA, or thromboembolism.
    vascular_disease : bool
        Prior MI, peripheral artery disease, or aortic plaque.
    sex : str
        ``'male'`` or ``'female'``.

    Returns
    -------
    dict
        ``score``         - int : CHA₂DS₂-VASc score (0-9).
        ``interpretation``- str : anticoagulation recommendation.
    """
    score = 0

    if chf:
        score += 1
    if hypertension:
        score += 1
    if age >= 75:
        score += 2
    elif age >= 65:
        score += 1
    if diabetes:
        score += 1
    if stroke_tia:
        score += 2
    if vascular_disease:
        score += 1
    if sex.lower() == "female":
        score += 1

    if score == 0:
        interpretation = (
            "Score 0: Low risk. Anticoagulation not recommended "
            "(male patients). Female sex alone does not warrant anticoagulation."
        )
    elif score == 1:
        interpretation = (
            "Score 1: Low-to-moderate risk. Consider anticoagulation "
            "based on individual patient factors and bleeding risk."
        )
    else:
        interpretation = (
            f"Score {score}: Moderate-to-high risk. "
            "Anticoagulation therapy is recommended."
        )

    return {"score": score, "interpretation": interpretation}


# =============================================================================
# ASCVD - 10-Year Cardiovascular Risk (ACC/AHA Pooled Cohort Equations)
#          (pre-implemented)
# =============================================================================

def calculate_ascvd_risk(age, sex, race, total_cholesterol, hdl_cholesterol,
                          systolic_bp, bp_treated, diabetes, smoker):
    """
    Estimate 10-year ASCVD risk using the ACC/AHA Pooled Cohort Equations.

    Calculates the 10-year risk of a first atherosclerotic cardiovascular
    event (non-fatal MI, coronary heart disease death, or fatal/non-fatal
    stroke) based on the 2013 ACC/AHA guidelines.

    Parameters
    ----------
    age : int
        Patient age in years (validated range 40-79).
    sex : str
        ``'male'`` or ``'female'``.
    race : str
        ``'white'`` or ``'aa'`` (African American).
    total_cholesterol : float
        Total cholesterol in mg/dL.
    hdl_cholesterol : float
        HDL cholesterol in mg/dL.
    systolic_bp : float
        Systolic blood pressure in mmHg.
    bp_treated : bool
        Whether the patient is currently on antihypertensive treatment.
    diabetes : bool
        Whether the patient has diabetes mellitus.
    smoker : bool
        Whether the patient is a current smoker.

    Returns
    -------
    dict
        ``risk_percentage`` - float : 10-year ASCVD risk as a percentage.
        ``interpretation``  - str   : statin therapy recommendation.

    Raises
    ------
    ValueError
        If ``sex`` is not ``'male'``/``'female'`` or ``race`` is not
        ``'white'``/``'aa'``.
    """
    ln_age = math.log(age)
    ln_total_chol = math.log(total_cholesterol)
    ln_hdl = math.log(hdl_cholesterol)
    ln_sbp = math.log(systolic_bp)
    is_smoker = int(bool(smoker))
    has_diabetes = int(bool(diabetes))

    sex_lower = sex.lower()
    race_lower = race.lower()

    if sex_lower == "female" and race_lower == "white":
        # White Women - Pooled Cohort Equation coefficients
        coeff_sum = (
            -29.799 * ln_age
            + 4.884 * (ln_age ** 2)
            + 13.540 * ln_total_chol
            + (-3.114) * ln_age * ln_total_chol
            + (-13.578) * ln_hdl
            + 3.149 * ln_age * ln_hdl
            + (2.019 * ln_sbp if bp_treated else 1.957 * ln_sbp)
            + 7.574 * is_smoker
            + (-1.665) * ln_age * is_smoker
            + 0.661 * has_diabetes
        )
        baseline_survival = 0.9665
        mean_coeff = -29.18

    elif sex_lower == "female" and race_lower == "aa":
        # African American Women - Pooled Cohort Equation coefficients
        coeff_sum = (
            17.1141 * ln_age
            + 0.9396 * ln_total_chol
            + (-18.9196) * ln_hdl
            + 4.4748 * ln_age * ln_hdl
            + (
                29.2907 * ln_sbp + (-6.4321) * ln_age * ln_sbp
                if bp_treated
                else 27.8197 * ln_sbp + (-6.0873) * ln_age * ln_sbp
            )
            + 0.8738 * is_smoker
            + 0.8738 * has_diabetes
        )
        baseline_survival = 0.9533
        mean_coeff = 86.61

    elif sex_lower == "male" and race_lower == "white":
        # White Men - Pooled Cohort Equation coefficients
        coeff_sum = (
            12.344 * ln_age
            + 11.853 * ln_total_chol
            + (-2.664) * ln_age * ln_total_chol
            + (-7.990) * ln_hdl
            + 1.769 * ln_age * ln_hdl
            + (1.797 * ln_sbp if bp_treated else 1.764 * ln_sbp)
            + 7.837 * is_smoker
            + (-1.795) * ln_age * is_smoker
            + 0.658 * has_diabetes
        )
        baseline_survival = 0.9144
        mean_coeff = 61.18

    elif sex_lower == "male" and race_lower == "aa":
        # African American Men - Pooled Cohort Equation coefficients
        coeff_sum = (
            2.469 * ln_age
            + 0.302 * ln_total_chol
            + (-0.307) * ln_hdl
            + (1.916 * ln_sbp if bp_treated else 1.809 * ln_sbp)
            + 0.549 * is_smoker
            + 0.645 * has_diabetes
        )
        baseline_survival = 0.8954
        mean_coeff = 19.54

    else:
        raise ValueError(
            "Invalid sex or race. "
            "sex must be 'male' or 'female'; race must be 'white' or 'aa'."
        )

    risk = 1.0 - baseline_survival ** math.exp(coeff_sum - mean_coeff)
    risk_pct = round(risk * 100, 1)

    if risk_pct < 5.0:
        interpretation = (
            f"10-year ASCVD risk: {risk_pct}% (Low risk). "
            "Lifestyle modifications recommended; statin therapy may not be necessary."
        )
    elif risk_pct < 7.5:
        interpretation = (
            f"10-year ASCVD risk: {risk_pct}% (Borderline risk). "
            "Discuss risk-enhancing factors; consider statin therapy."
        )
    elif risk_pct < 20.0:
        interpretation = (
            f"10-year ASCVD risk: {risk_pct}% (Intermediate risk). "
            "Moderate-intensity statin therapy recommended."
        )
    else:
        interpretation = (
            f"10-year ASCVD risk: {risk_pct}% (High risk). "
            "High-intensity statin therapy recommended."
        )

    return {"risk_percentage": risk_pct, "interpretation": interpretation}


# =============================================================================
# HEART Score - Major Adverse Cardiac Events  (STUDENT TODO)
# =============================================================================

def calculate_heart_score(history, ecg, age_score, risk_factors, troponin):
    """
    Calculate HEART Score for Major Adverse Cardiac Events (MACE).

    The HEART score risk-stratifies patients presenting with chest pain for
    the likelihood of a major adverse cardiac event (MACE) — defined as
    acute MI, PCI, CABG, or death — within 6 weeks.

    Each component is already converted to its numeric 0 / 1 / 2 value
    before being passed to this function.

    Parameters
    ----------
    history : int
        Clinical suspicion based on history:
          0 = Slightly suspicious (mostly non-specific)
          1 = Moderately suspicious
          2 = Highly suspicious (classic ACS presentation)
    ecg : int
        ECG findings:
          0 = Normal
          1 = Non-specific repolarisation disturbance
          2 = Significant ST deviation
    age_score : int
        Age category:
          0 = Age < 45
          1 = Age 45-64
          2 = Age ≥ 65
    risk_factors : int
        Known cardiovascular risk factors
        (hypertension, hypercholesterolaemia, diabetes, obesity BMI > 30,
         smoking, positive family history of CAD, known atherosclerotic
         disease):
          0 = No known risk factors
          1 = 1–2 risk factors, or obesity (BMI > 30)
          2 = ≥ 3 risk factors, history of DM, or known atherosclerotic
              disease (prior PCI/CABG, stroke, PAD)
    troponin : int
        Initial troponin level relative to the assay's normal limit:
          0 = ≤ normal limit
          1 = 1-3 x normal limit
          2 = > 3 x normal limit

    Returns
    -------
    dict
        ``score``         - int : total HEART score (0-10).
        ``risk_level``    - str : ``'low'``, ``'moderate'``, or ``'high'``.
        ``interpretation``- str : clinical management recommendation.

    Raises
    ------
    ValueError
        If any parameter value is not 0, 1, or 2.

    Score Interpretation
    --------------------
    0-3  : Low risk      (~1.7 % MACE) - consider early discharge
    4-6  : Moderate risk (~12 % MACE)  - observe; serial troponins
    7-10 : High risk     (~65 % MACE)  - early invasive strategy

    TODO for Students
    -----------------
    Implement this function using the parameter descriptions above.

    Steps:
      1. Validate that *each* parameter (history, ecg, age_score,
         risk_factors, troponin) is an integer with value 0, 1, or 2.
         If any value is outside this range, raise a ``ValueError``.
      2. Sum all five parameters to compute the total HEART score.
      3. Determine the risk level:
           score 0-3  → ``'low'``
           score 4-6  → ``'moderate'``
           score 7-10 → ``'high'``
      4. Build the ``interpretation`` string with the clinical
         recommendation matching the risk level.
      5. Return a dict containing ``'score'``, ``'risk_level'``, and
         ``'interpretation'``.
    """
    components = {
        "history": history,
        "ecg": ecg,
        "age_score": age_score,
        "risk_factors": risk_factors,
        "troponin": troponin,
    }

    for value in components.values():
        if not isinstance(value, int) or value < 0 or value > 2:
            raise ValueError(
                "HEART Score components must each be an integer value of 0, 1, or 2."
            )

    score = sum(components.values())

    if score <= 3:
        risk_level = "low"
        interpretation = (
            f"HEART score {score}: Low risk (~1.7% MACE). "
            "Consider early discharge if clinically appropriate."
        )
    elif score <= 6:
        risk_level = "moderate"
        interpretation = (
            f"HEART score {score}: Moderate risk (~12% MACE). "
            "Observe the patient and obtain serial troponins."
        )
    else:
        risk_level = "high"
        interpretation = (
            f"HEART score {score}: High risk (~65% MACE). "
            "Early invasive strategy is recommended."
        )

    return {
        "score": score,
        "risk_level": risk_level,
        "interpretation": interpretation,
    }


# =============================================================================
# PECARN - Pediatric Head Injury Decision Rule  (STUDENT TODO)
# =============================================================================

def calculate_pecarn(age_months, gcs, altered_mental_status,
                     loss_of_consciousness, palpable_skull_fracture,
                     scalp_hematoma_location, severe_mechanism,
                     vomiting, severe_headache, signs_basal_skull_fracture):
    """
    Apply the PECARN Pediatric Head Injury Decision Rule.

    The PECARN rule identifies children at very low risk of clinically
    important traumatic brain injury (ciTBI) for whom CT can be safely
    avoided, thereby reducing unnecessary radiation exposure.

    The rule differs for children **younger than 24 months** versus those
    **24 months and older**.

    Parameters
    ----------
    age_months : int
        Patient age in months.
    gcs : int
        Glasgow Coma Scale score (valid range 3-15).
    altered_mental_status : bool
        Agitation, somnolence, repetitive questioning, or slowed response
        to verbal communication.
    loss_of_consciousness : bool
        Any loss of consciousness after the injury.
    palpable_skull_fracture : bool
        Palpable skull fracture on physical examination.
        (Used for age < 24 months.)
    scalp_hematoma_location : str
        Location of scalp hematoma: ``'frontal'``, ``'non-frontal'``,
        or ``'none'``.
        (Used for age < 24 months; non-frontal hematomas carry intermediate
        risk, frontal hematomas do not.)
    severe_mechanism : bool
        Severe mechanism of injury:
          - Age < 24 months : fall > 3 ft, or head struck by high-impact
            object.
          - Age ≥ 24 months : fall > 5 ft; MVA with ejection, rollover, or
            fatality; pedestrian or cyclist vs. vehicle; head struck by
            high-impact object.
    vomiting : bool
        Vomiting after the injury.
    severe_headache : bool
        Severe headache reported by the child.
        (Used for age ≥ 24 months.)
    signs_basal_skull_fracture : bool
        Signs of basilar skull fracture: haemotympanum, 'raccoon eyes',
        retroauricular bruising (Battle's sign), or CSF
        otorrhoea/rhinorrhoea.
        (Used for age ≥ 24 months.)

    Returns
    -------
    dict
        ``risk_level``   - str : ``'high'``, ``'intermediate'``, or
                                 ``'low'``.
        ``recommendation``- str : CT management recommendation.
        ``interpretation``- str : detailed plain-language explanation.

    Raises
    ------
    ValueError
        If ``gcs`` is not between 3 and 15 (inclusive).

    Risk Levels
    -----------
    high         : CT scan recommended.
    intermediate : CT vs. observation — individualise based on physician
                   experience, number of findings, symptom trajectory,
                   child age < 3 months, and parental preference.
    low          : CT scan NOT recommended (very low risk of ciTBI < 0.02 %).

    Decision Rules
    --------------
    **Age < 24 months**

    HIGH risk (CT recommended) if **any** of:
      • GCS < 15
      • Palpable skull fracture
      • Altered mental status

    INTERMEDIATE risk if **any** of:
      • Loss of consciousness
      • Non-frontal scalp hematoma
      • Severe mechanism of injury
      • Vomiting

    LOW risk: none of the above.

    **Age ≥ 24 months**

    HIGH risk (CT recommended) if **any** of:
      • GCS < 15
      • Signs of basilar skull fracture
      • Altered mental status

    INTERMEDIATE risk if **any** of:
      • Loss of consciousness
      • Vomiting
      • Severe mechanism of injury
      • Severe headache

    LOW risk: none of the above.

    TODO for Students
    -----------------
    Implement this function using the decision rules described above.

    Steps:
      1. Validate that ``gcs`` is between 3 and 15 (inclusive).
         If not, raise a ``ValueError``.
      2. Check ``age_months < 24``:
           a. HIGH risk if GCS < 15, palpable_skull_fracture, or
              altered_mental_status.
           b. INTERMEDIATE risk (if not high) if loss_of_consciousness,
              scalp_hematoma_location == 'non-frontal', severe_mechanism,
              or vomiting.
           c. Otherwise: LOW risk.
      3. If ``age_months >= 24``:
           a. HIGH risk if GCS < 15, signs_basal_skull_fracture, or
              altered_mental_status.
           b. INTERMEDIATE risk (if not high) if loss_of_consciousness,
              vomiting, severe_mechanism, or severe_headache.
           c. Otherwise: LOW risk.
      4. Return a dict with ``'risk_level'``, ``'recommendation'``, and
         ``'interpretation'`` using these exact recommendation strings:
           high         → 'CT scan recommended'
           intermediate → 'CT scan versus observation: individualise based on
                           physician experience, multiple vs isolated findings,
                           worsening symptoms, age < 3 months, parental
                           preference'
           low          → 'CT scan NOT recommended'
    """
    if gcs < 3 or gcs > 15:
        raise ValueError("gcs must be between 3 and 15 inclusive.")

    if age_months < 24:
        if gcs < 15 or palpable_skull_fracture or altered_mental_status:
            risk_level = "high"
        elif (
            loss_of_consciousness
            or scalp_hematoma_location == "non-frontal"
            or severe_mechanism
            or vomiting
        ):
            risk_level = "intermediate"
        else:
            risk_level = "low"
    else:
        if gcs < 15 or signs_basal_skull_fracture or altered_mental_status:
            risk_level = "high"
        elif loss_of_consciousness or vomiting or severe_mechanism or severe_headache:
            risk_level = "intermediate"
        else:
            risk_level = "low"

    recommendation_map = {
        "high": "CT scan recommended",
        "intermediate": (
            "CT scan versus observation: individualise based on physician "
            "experience, multiple vs isolated findings, worsening symptoms, "
            "age < 3 months, parental preference"
        ),
        "low": "CT scan NOT recommended",
    }

    interpretation_map = {
        "high": (
            "High risk for clinically important traumatic brain injury. "
            "CT imaging is recommended."
        ),
        "intermediate": (
            "Intermediate risk for clinically important traumatic brain injury. "
            "Consider CT versus observation based on the full clinical picture."
        ),
        "low": (
            "Low risk for clinically important traumatic brain injury. "
            "CT imaging is not recommended."
        ),
    }

    return {
        "risk_level": risk_level,
        "recommendation": recommendation_map[risk_level],
        "interpretation": interpretation_map[risk_level],
    }
