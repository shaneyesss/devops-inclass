"""
Tests for Clinical Risk Score Calculators
==========================================

Run all tests:
    pytest test_calculators.py -v

NOTE
----
Tests for ``calculate_heart_score()`` and ``calculate_pecarn()`` will
**FAIL** until you implement those two functions in ``calculators.py``.
That is intentional — it demonstrates the power of Continuous Integration!

Once you implement both functions and push to the ``main`` branch, the
GitHub Actions workflow will run these tests automatically. All tests must
pass before the push is accepted.
"""

import pytest

from calculators import (
    calculate_ascvd_risk,
    calculate_chads_vasc,
    calculate_heart_score,
    calculate_pecarn,
    calculate_perc,
)


# =============================================================================
# PERC Tests  (pre-implemented – these should pass from the start)
# =============================================================================

class TestPERC:
    """Tests for the PE Rule-Out Criteria (PERC) calculator."""

    def test_perc_negative_all_low_risk(self):
        """A patient with all low-risk values should be PERC negative (score 0)."""
        result = calculate_perc(
            age=40, heart_rate=80, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["score"] == 0
        assert result["perc_negative"] is True

    def test_perc_positive_age_criterion(self):
        """Age ≥ 50 triggers the age criterion → PERC positive."""
        result = calculate_perc(
            age=50, heart_rate=80, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["score"] == 1
        assert result["perc_negative"] is False

    def test_perc_positive_tachycardia(self):
        """Heart rate ≥ 100 bpm triggers the HR criterion."""
        result = calculate_perc(
            age=40, heart_rate=100, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["perc_negative"] is False

    def test_perc_positive_low_o2_saturation(self):
        """O₂ saturation < 95 % triggers the oxygen criterion."""
        result = calculate_perc(
            age=40, heart_rate=80, o2_sat=94,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["perc_negative"] is False

    def test_perc_positive_multiple_criteria(self):
        """Multiple positive criteria accumulate in the score."""
        result = calculate_perc(
            age=55, heart_rate=105, o2_sat=93,
            hemoptysis=True, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["score"] == 4
        assert result["perc_negative"] is False

    def test_perc_all_criteria_positive(self):
        """All eight criteria positive → score 8."""
        result = calculate_perc(
            age=55, heart_rate=105, o2_sat=93,
            hemoptysis=True, estrogen_use=True, prior_dvt_pe=True,
            unilateral_leg_swelling=True, surgery_trauma_4wks=True,
        )
        assert result["score"] == 8
        assert result["perc_negative"] is False

    def test_perc_boundary_age_49(self):
        """Age 49 does NOT trigger the age criterion."""
        result = calculate_perc(
            age=49, heart_rate=80, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["perc_negative"] is True

    def test_perc_boundary_o2_exactly_95(self):
        """O₂ saturation of exactly 95 % does NOT trigger criterion (rule: < 95)."""
        result = calculate_perc(
            age=40, heart_rate=80, o2_sat=95,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["perc_negative"] is True

    def test_perc_boundary_hr_99(self):
        """Heart rate of 99 does NOT trigger the HR criterion (rule: ≥ 100)."""
        result = calculate_perc(
            age=40, heart_rate=99, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert result["perc_negative"] is True

    def test_perc_result_contains_required_keys(self):
        """Result dict must contain 'score', 'perc_negative', and 'interpretation'."""
        result = calculate_perc(
            age=40, heart_rate=80, o2_sat=97,
            hemoptysis=False, estrogen_use=False, prior_dvt_pe=False,
            unilateral_leg_swelling=False, surgery_trauma_4wks=False,
        )
        assert "score" in result
        assert "perc_negative" in result
        assert "interpretation" in result
        assert isinstance(result["interpretation"], str)


# =============================================================================
# CHA₂DS₂-VASc Tests  (pre-implemented – these should pass from the start)
# =============================================================================

class TestCHADSVASc:
    """Tests for the CHA₂DS₂-VASc atrial fibrillation stroke risk calculator."""

    def test_score_zero_young_male_no_risk_factors(self):
        """Young male with no risk factors should score 0."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=50,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 0

    def test_female_sex_adds_one_point(self):
        """Female sex category adds 1 point."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=50,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="female",
        )
        assert result["score"] == 1

    def test_chf_adds_one_point(self):
        """Congestive heart failure adds 1 point."""
        result = calculate_chads_vasc(
            chf=True, hypertension=False, age=50,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 1

    def test_hypertension_adds_one_point(self):
        """Hypertension adds 1 point."""
        result = calculate_chads_vasc(
            chf=False, hypertension=True, age=50,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 1

    def test_age_65_to_74_adds_one_point(self):
        """Age 65–74 adds 1 point."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=68,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 1

    def test_age_75_or_older_adds_two_points(self):
        """Age ≥ 75 adds 2 points."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=75,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 2

    def test_stroke_tia_adds_two_points(self):
        """Prior stroke or TIA adds 2 points."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=50,
            diabetes=False, stroke_tia=True,
            vascular_disease=False, sex="male",
        )
        assert result["score"] == 2

    def test_maximum_score_all_risk_factors(self):
        """All risk factors should yield the maximum score of 9."""
        result = calculate_chads_vasc(
            chf=True, hypertension=True, age=76,
            diabetes=True, stroke_tia=True,
            vascular_disease=True, sex="female",
        )
        assert result["score"] == 9

    def test_typical_high_risk_afib_patient(self):
        """Hypertensive female aged 70 with vascular disease scores 4."""
        result = calculate_chads_vasc(
            chf=False, hypertension=True, age=70,
            diabetes=False, stroke_tia=False,
            vascular_disease=True, sex="female",
        )
        # HTN=1, age 65-74=1, vascular_disease=1, female=1 → 4
        assert result["score"] == 4

    def test_result_contains_required_keys(self):
        """Result must contain 'score' and 'interpretation'."""
        result = calculate_chads_vasc(
            chf=False, hypertension=False, age=50,
            diabetes=False, stroke_tia=False,
            vascular_disease=False, sex="male",
        )
        assert "score" in result
        assert "interpretation" in result
        assert isinstance(result["interpretation"], str)


# =============================================================================
# ASCVD Tests  (pre-implemented – these should pass from the start)
# =============================================================================

class TestASCVD:
    """Tests for the 10-year ASCVD risk calculator (Pooled Cohort Equations)."""

    def test_white_male_low_risk(self):
        """Young white male with favourable lipids and BP should be low risk."""
        result = calculate_ascvd_risk(
            age=45, sex="male", race="white",
            total_cholesterol=170, hdl_cholesterol=60,
            systolic_bp=115, bp_treated=False,
            diabetes=False, smoker=False,
        )
        assert result["risk_percentage"] < 7.5

    def test_white_female_low_risk(self):
        """Middle-aged white female with favourable values should be low risk."""
        result = calculate_ascvd_risk(
            age=55, sex="female", race="white",
            total_cholesterol=175, hdl_cholesterol=65,
            systolic_bp=118, bp_treated=False,
            diabetes=False, smoker=False,
        )
        assert result["risk_percentage"] < 7.5

    def test_aa_male_elevated_risk(self):
        """Older African-American male with multiple risk factors should be elevated."""
        result = calculate_ascvd_risk(
            age=65, sex="male", race="aa",
            total_cholesterol=220, hdl_cholesterol=40,
            systolic_bp=150, bp_treated=False,
            diabetes=True, smoker=True,
        )
        assert result["risk_percentage"] >= 7.5

    def test_aa_female_elevated_risk(self):
        """Older African-American female with multiple risk factors should be elevated."""
        result = calculate_ascvd_risk(
            age=65, sex="female", race="aa",
            total_cholesterol=220, hdl_cholesterol=40,
            systolic_bp=150, bp_treated=False,
            diabetes=True, smoker=True,
        )
        assert result["risk_percentage"] >= 7.5

    def test_invalid_sex_raises_value_error(self):
        """An unrecognised sex string should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_ascvd_risk(
                age=55, sex="unknown", race="white",
                total_cholesterol=200, hdl_cholesterol=50,
                systolic_bp=130, bp_treated=False,
                diabetes=False, smoker=False,
            )

    def test_invalid_race_raises_value_error(self):
        """An unrecognised race string should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_ascvd_risk(
                age=55, sex="male", race="hispanic",
                total_cholesterol=200, hdl_cholesterol=50,
                systolic_bp=130, bp_treated=False,
                diabetes=False, smoker=False,
            )

    def test_bp_treatment_changes_risk(self):
        """Treated vs untreated BP should produce different risk estimates."""
        common = dict(
            age=60, sex="male", race="white",
            total_cholesterol=200, hdl_cholesterol=50,
            systolic_bp=145, diabetes=False, smoker=False,
        )
        result_treated = calculate_ascvd_risk(**common, bp_treated=True)
        result_untreated = calculate_ascvd_risk(**common, bp_treated=False)
        assert result_treated["risk_percentage"] != result_untreated["risk_percentage"]

    def test_result_contains_required_keys(self):
        """Result must contain 'risk_percentage' and 'interpretation'."""
        result = calculate_ascvd_risk(
            age=50, sex="male", race="white",
            total_cholesterol=200, hdl_cholesterol=50,
            systolic_bp=130, bp_treated=False,
            diabetes=False, smoker=False,
        )
        assert "risk_percentage" in result
        assert "interpretation" in result
        assert isinstance(result["risk_percentage"], float)

    def test_risk_percentage_is_between_0_and_100(self):
        """Risk percentage must always be in [0, 100]."""
        result = calculate_ascvd_risk(
            age=55, sex="male", race="white",
            total_cholesterol=200, hdl_cholesterol=50,
            systolic_bp=130, bp_treated=False,
            diabetes=False, smoker=False,
        )
        assert 0.0 <= result["risk_percentage"] <= 100.0


# =============================================================================
# HEART Score Tests  ← Students must implement calculate_heart_score()
# =============================================================================

class TestHEARTScore:
    """
    Tests for the HEART score calculator.

    **These tests will FAIL until you implement** ``calculate_heart_score()``
    **in** ``calculators.py``.
    """

    def test_all_zeros_gives_score_zero(self):
        """All components scored 0 should yield a total score of 0."""
        result = calculate_heart_score(
            history=0, ecg=0, age_score=0, risk_factors=0, troponin=0,
        )
        assert result["score"] == 0

    def test_score_zero_is_low_risk(self):
        """A score of 0 should be classified as low risk."""
        result = calculate_heart_score(
            history=0, ecg=0, age_score=0, risk_factors=0, troponin=0,
        )
        assert result["risk_level"] == "low"

    def test_score_three_is_low_risk_boundary(self):
        """A score of 3 is the upper boundary for low risk."""
        result = calculate_heart_score(
            history=1, ecg=1, age_score=1, risk_factors=0, troponin=0,
        )
        assert result["score"] == 3
        assert result["risk_level"] == "low"

    def test_score_four_is_moderate_risk_boundary(self):
        """A score of 4 is the lower boundary for moderate risk."""
        result = calculate_heart_score(
            history=2, ecg=1, age_score=1, risk_factors=0, troponin=0,
        )
        assert result["score"] == 4
        assert result["risk_level"] == "moderate"

    def test_score_six_is_moderate_risk_upper_boundary(self):
        """A score of 6 is the upper boundary for moderate risk."""
        result = calculate_heart_score(
            history=2, ecg=2, age_score=2, risk_factors=0, troponin=0,
        )
        assert result["score"] == 6
        assert result["risk_level"] == "moderate"

    def test_score_seven_is_high_risk_boundary(self):
        """A score of 7 is the lower boundary for high risk."""
        result = calculate_heart_score(
            history=2, ecg=2, age_score=1, risk_factors=1, troponin=1,
        )
        assert result["score"] == 7
        assert result["risk_level"] == "high"

    def test_maximum_score_ten_is_high_risk(self):
        """All components scored 2 yields total score 10 (maximum) – high risk."""
        result = calculate_heart_score(
            history=2, ecg=2, age_score=2, risk_factors=2, troponin=2,
        )
        assert result["score"] == 10
        assert result["risk_level"] == "high"

    def test_typical_moderate_risk_patient(self):
        """Typical moderate-risk chest pain presentation scores 5."""
        result = calculate_heart_score(
            history=2, ecg=1, age_score=1, risk_factors=1, troponin=0,
        )
        assert result["score"] == 5
        assert result["risk_level"] == "moderate"

    def test_invalid_history_value_raises_error(self):
        """A component value of 3 should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_heart_score(
                history=3, ecg=0, age_score=0, risk_factors=0, troponin=0,
            )

    def test_negative_component_raises_error(self):
        """A negative component value should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_heart_score(
                history=0, ecg=-1, age_score=0, risk_factors=0, troponin=0,
            )

    def test_result_contains_required_keys(self):
        """Result must contain 'score', 'risk_level', and 'interpretation'."""
        result = calculate_heart_score(
            history=1, ecg=1, age_score=1, risk_factors=1, troponin=1,
        )
        assert "score" in result
        assert "risk_level" in result
        assert "interpretation" in result
        assert isinstance(result["interpretation"], str)


# =============================================================================
# PECARN Tests  ← Students must implement calculate_pecarn()
# =============================================================================

class TestPECARN:
    """
    Tests for the PECARN paediatric head injury decision rule.

    **These tests will FAIL until you implement** ``calculate_pecarn()``
    **in** ``calculators.py``.
    """

    # ---- Children under 24 months ----------------------------------------

    def test_under2_high_risk_low_gcs(self):
        """Child < 24 months with GCS < 15 → high risk."""
        result = calculate_pecarn(
            age_months=18, gcs=14, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"

    def test_under2_high_risk_palpable_skull_fracture(self):
        """Child < 24 months with palpable skull fracture → high risk."""
        result = calculate_pecarn(
            age_months=12, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=True,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"

    def test_under2_high_risk_altered_mental_status(self):
        """Child < 24 months with altered mental status → high risk."""
        result = calculate_pecarn(
            age_months=6, gcs=15, altered_mental_status=True,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"

    def test_under2_intermediate_risk_loss_of_consciousness(self):
        """Child < 24 months with LOC only (no high-risk features) → intermediate."""
        result = calculate_pecarn(
            age_months=18, gcs=15, altered_mental_status=False,
            loss_of_consciousness=True, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "intermediate"

    def test_under2_intermediate_risk_non_frontal_hematoma(self):
        """Child < 24 months with non-frontal scalp hematoma → intermediate."""
        result = calculate_pecarn(
            age_months=18, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="non-frontal", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "intermediate"

    def test_under2_intermediate_risk_severe_mechanism(self):
        """Child < 24 months with severe mechanism → intermediate."""
        result = calculate_pecarn(
            age_months=18, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=True,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "intermediate"

    def test_under2_frontal_hematoma_is_low_risk(self):
        """Frontal scalp hematoma in child < 24 months is NOT an intermediate risk factor."""
        result = calculate_pecarn(
            age_months=18, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="frontal", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "low"

    def test_under2_low_risk_no_factors(self):
        """Child < 24 months with no risk factors → low risk."""
        result = calculate_pecarn(
            age_months=18, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "low"

    # ---- Children 24 months and older ------------------------------------

    def test_over2_high_risk_low_gcs(self):
        """Child ≥ 24 months with GCS < 15 → high risk."""
        result = calculate_pecarn(
            age_months=36, gcs=13, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"

    def test_over2_high_risk_basilar_skull_fracture_signs(self):
        """Child ≥ 24 months with signs of basilar skull fracture → high risk."""
        result = calculate_pecarn(
            age_months=48, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=True,
        )
        assert result["risk_level"] == "high"

    def test_over2_high_risk_altered_mental_status(self):
        """Child ≥ 24 months with altered mental status → high risk."""
        result = calculate_pecarn(
            age_months=60, gcs=15, altered_mental_status=True,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"

    def test_over2_intermediate_risk_vomiting(self):
        """Child ≥ 24 months with vomiting only → intermediate risk."""
        result = calculate_pecarn(
            age_months=60, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=True, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "intermediate"

    def test_over2_intermediate_risk_severe_headache(self):
        """Child ≥ 24 months with severe headache only → intermediate risk."""
        result = calculate_pecarn(
            age_months=60, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=True,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "intermediate"

    def test_over2_low_risk_no_factors(self):
        """Child ≥ 24 months with no risk factors → low risk."""
        result = calculate_pecarn(
            age_months=48, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "low"

    # ---- Validation -------------------------------------------------------

    def test_gcs_below_3_raises_value_error(self):
        """GCS value below 3 should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_pecarn(
                age_months=24, gcs=2, altered_mental_status=False,
                loss_of_consciousness=False, palpable_skull_fracture=False,
                scalp_hematoma_location="none", severe_mechanism=False,
                vomiting=False, severe_headache=False,
                signs_basal_skull_fracture=False,
            )

    def test_gcs_above_15_raises_value_error(self):
        """GCS value above 15 should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_pecarn(
                age_months=24, gcs=16, altered_mental_status=False,
                loss_of_consciousness=False, palpable_skull_fracture=False,
                scalp_hematoma_location="none", severe_mechanism=False,
                vomiting=False, severe_headache=False,
                signs_basal_skull_fracture=False,
            )

    def test_result_contains_required_keys(self):
        """Result must contain 'risk_level', 'recommendation', and 'interpretation'."""
        result = calculate_pecarn(
            age_months=48, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert "risk_level" in result
        assert "recommendation" in result
        assert "interpretation" in result

    def test_high_risk_recommendation_mentions_ct(self):
        """High-risk recommendation string should reference CT scan."""
        result = calculate_pecarn(
            age_months=48, gcs=14, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "high"
        assert "CT" in result["recommendation"]

    def test_low_risk_recommendation_advises_against_ct(self):
        """Low-risk recommendation string should advise against CT scan."""
        result = calculate_pecarn(
            age_months=48, gcs=15, altered_mental_status=False,
            loss_of_consciousness=False, palpable_skull_fracture=False,
            scalp_hematoma_location="none", severe_mechanism=False,
            vomiting=False, severe_headache=False,
            signs_basal_skull_fracture=False,
        )
        assert result["risk_level"] == "low"
        assert "NOT" in result["recommendation"]
