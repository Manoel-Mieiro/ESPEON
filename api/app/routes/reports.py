from flask import Blueprint, request, jsonify
from app.controllers import reports as reportController

report_bp = Blueprint("report_bp", __name__, url_prefix="/reports")


@report_bp.route("/", methods=["GET"])
def get_all_reports():
    try:
        return jsonify(reportController.findAllReports()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/", methods=["POST"])
def create_report():
    try:
        data = request.get_json()
        return jsonify(reportController.createReport(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/<report_id>", methods=["GET"])
def get_report(report_id):
    try:
        return jsonify(reportController.findOneReport(report_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@report_bp.route("/<report_id>", methods=["PUT"])
def update_report(report_id):
    try:
        data = request.get_json()
        return jsonify(reportController.updateReport(report_id, data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/<report_id>", methods=["DELETE"])
def delete_report(report_id):
    try:
        return jsonify(reportController.deleteReport(report_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route("/pdf/<report_id>", methods=["GET"])
def get_report_pdf(report_id):
    try:
        return reportController.getReportPdf(report_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500