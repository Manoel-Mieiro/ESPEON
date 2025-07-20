from flask import jsonify, Blueprint, request
import app.controllers.reports as reportController

reports_bp = Blueprint("reports", __name__)

kinds = ["student", "lecture", "subject"]

@reports_bp.route("/reports/<kind>", methods=["GET"])
def listReports(kind):
    try:
        if kind not in kinds:
            return jsonify("Page not Found"), 404
        reports = reportController.listReports(kind)
        if reports:
            return jsonify(reports), 200
        else:
            return jsonify([]), 204
    except Exception as e:
        return jsonify({"error": f"[ROUTES] {str(e)}"}), 500


@reports_bp.route("/reports/<kind>/<subject>", methods=["GET"])
def createReport(kind, subject):
    try:
        if kind not in kinds:
            return jsonify("Page not Found"), 404

        report = reportController.createReports(kind, subject)
        return jsonify(report), 201
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500
