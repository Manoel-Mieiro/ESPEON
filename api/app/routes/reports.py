from flask import jsonify, Blueprint, request
import app.controllers.reports as reportController

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/<kind>", methods=["GET"])
def listReports(kind):
    try:
        reports = reportController.listReports(kind)
        if reports:
            return jsonify(reports), 200
        else:
            return jsonify([]), 204
    except Exception as e:
        return jsonify({"error": f"[ROUTES] {str(e)}"}), 500


@reports_bp.route("/reports<kind>", methods=["POST"])
def createReport(kind):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        new_trace = reportController.createReports(data, kind)
        return jsonify(new_trace), 201
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500
