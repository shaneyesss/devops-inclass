"""
Clinical Risk Score Calculators – Flask Application
=====================================================

A REST API and simple web front-end for five widely used clinical risk
score calculators:

  • PERC Rule     - PE Rule-Out Criteria
  • HEART Score   - Major Adverse Cardiac Events
  • CHA₂DS₂-VASc - Atrial Fibrillation Stroke Risk
  • ASCVD Risk    - 10-Year Cardiovascular Risk (Pooled Cohort Equations)
  • PECARN        - Pediatric Head Injury Decision Rule

Run the development server:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os

from flask import Flask, jsonify, request, send_from_directory

from calculators import (
    calculate_ascvd_risk,
    calculate_chads_vasc,
    calculate_heart_score,
    calculate_pecarn,
    calculate_perc,
)

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(app.root_path, "index.html")


@app.route("/styles.css")
def styles():
    return send_from_directory(app.root_path, "styles.css")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _bad_json():
    return jsonify({"error": "Request body must be valid JSON."}), 400


def _missing(field):
    return jsonify({"error": f"Missing required field: {field}"}), 400


# ---------------------------------------------------------------------------
# /api/perc
# ---------------------------------------------------------------------------

@app.route("/api/perc", methods=["POST"])
def perc_route():
    data = request.get_json(silent=True)
    if data is None:
        return _bad_json()
    required = [
        "age", "heart_rate", "o2_sat", "hemoptysis",
        "estrogen_use", "prior_dvt_pe",
        "unilateral_leg_swelling", "surgery_trauma_4wks",
    ]
    for field in required:
        if field not in data:
            return _missing(field)
    try:
        result = calculate_perc(
            age=data["age"],
            heart_rate=data["heart_rate"],
            o2_sat=data["o2_sat"],
            hemoptysis=data["hemoptysis"],
            estrogen_use=data["estrogen_use"],
            prior_dvt_pe=data["prior_dvt_pe"],
            unilateral_leg_swelling=data["unilateral_leg_swelling"],
            surgery_trauma_4wks=data["surgery_trauma_4wks"],
        )
        return jsonify(result)
    except Exception:
        return jsonify({"error": "An unexpected error occurred."}), 500
# ---------------------------------------------------------------------------

@app.route("/api/heart", methods=["POST"])
def heart_route():
    data = request.get_json(silent=True)
    if data is None:
        return _bad_json()
    required = ["history", "ecg", "age_score", "risk_factors", "troponin"]
    for field in required:
        if field not in data:
            return _missing(field)
    try:
        result = calculate_heart_score(
            history=data["history"],
            ecg=data["ecg"],
            age_score=data["age_score"],
            risk_factors=data["risk_factors"],
            troponin=data["troponin"],
        )
        return jsonify(result)
    except NotImplementedError as exc:
        return jsonify({"error": str(exc)}), 501
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# /api/chads_vasc
# ---------------------------------------------------------------------------

@app.route("/api/chads_vasc", methods=["POST"])
def chads_vasc_route():
    data = request.get_json(silent=True)
    if data is None:
        return _bad_json()
    required = [
        "chf", "hypertension", "age", "diabetes",
        "stroke_tia", "vascular_disease", "sex",
    ]
    for field in required:
        if field not in data:
            return _missing(field)
    try:
        result = calculate_chads_vasc(
            chf=data["chf"],
            hypertension=data["hypertension"],
            age=data["age"],
            diabetes=data["diabetes"],
            stroke_tia=data["stroke_tia"],
            vascular_disease=data["vascular_disease"],
            sex=data["sex"],
        )
        return jsonify(result)
    except Exception:
        return jsonify({"error": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# /api/ascvd
# ---------------------------------------------------------------------------

@app.route("/api/ascvd", methods=["POST"])
def ascvd_route():
    data = request.get_json(silent=True)
    if data is None:
        return _bad_json()
    required = [
        "age", "sex", "race", "total_cholesterol",
        "hdl_cholesterol", "systolic_bp", "bp_treated",
        "diabetes", "smoker",
    ]
    for field in required:
        if field not in data:
            return _missing(field)
    try:
        result = calculate_ascvd_risk(
            age=data["age"],
            sex=data["sex"],
            race=data["race"],
            total_cholesterol=data["total_cholesterol"],
            hdl_cholesterol=data["hdl_cholesterol"],
            systolic_bp=data["systolic_bp"],
            bp_treated=data["bp_treated"],
            diabetes=data["diabetes"],
            smoker=data["smoker"],
        )
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# /api/pecarn
# ---------------------------------------------------------------------------

@app.route("/api/pecarn", methods=["POST"])
def pecarn_route():
    data = request.get_json(silent=True)
    if data is None:
        return _bad_json()
    required = [
        "age_months", "gcs", "altered_mental_status",
        "loss_of_consciousness", "palpable_skull_fracture",
        "scalp_hematoma_location", "severe_mechanism",
        "vomiting", "severe_headache", "signs_basal_skull_fracture",
    ]
    for field in required:
        if field not in data:
            return _missing(field)
    try:
        result = calculate_pecarn(
            age_months=data["age_months"],
            gcs=data["gcs"],
            altered_mental_status=data["altered_mental_status"],
            loss_of_consciousness=data["loss_of_consciousness"],
            palpable_skull_fracture=data["palpable_skull_fracture"],
            scalp_hematoma_location=data["scalp_hematoma_location"],
            severe_mechanism=data["severe_mechanism"],
            vomiting=data["vomiting"],
            severe_headache=data["severe_headache"],
            signs_basal_skull_fracture=data["signs_basal_skull_fracture"],
        )
        return jsonify(result)
    except NotImplementedError as exc:
        return jsonify({"error": str(exc)}), 501
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Use FLASK_DEBUG=true environment variable to enable debug mode.
    # Never enable debug mode in production.
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
