from flask import Blueprint, request, jsonify
from app.controllers import reportsStudent as reportStudentController

report_student_bp = Blueprint("report_student_bp", __name__, url_prefix="/reports/students")


@report_student_bp.route("/", methods=["GET"])
def get_all_student_reports():
    try:
        return jsonify(reportStudentController.findAllStudentReports()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_student_bp.route("/", methods=["POST"])
def create_student_report():
    try:
        data = request.get_json()
        return jsonify(reportStudentController.createStudentReport(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_student_bp.route("/<report_student_id>", methods=["GET"])
def get_student_report(report_student_id):
    try:
        return jsonify(reportStudentController.findOneStudentReport(report_student_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@report_student_bp.route("/<report_student_id>", methods=["PUT"])
def update_student_report(report_student_id):
    try:
        data = request.get_json()
        return jsonify(reportStudentController.updateStudentReport(report_student_id, data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_student_bp.route("/<report_student_id>", methods=["DELETE"])
def delete_student_report(report_student_id):
    try:
        return jsonify(reportStudentController.deleteStudentReport(report_student_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
