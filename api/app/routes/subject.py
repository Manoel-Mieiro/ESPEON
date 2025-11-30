from flask import jsonify, Blueprint, request
import app.controllers.subject as subjectController
from app.swagger.subjects import register_swagger_routes

subjects_bp = Blueprint("subjects", __name__)

subjects_ns = register_swagger_routes()

@subjects_bp.route("/subjects", methods=["GET"])
def get_all_subjects():
    try:
        return jsonify(subjectController.findAllSubjects()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subjects_bp.route("/subjects/<subject_id>", methods=["GET"])
def get_one_subject(subject_id):
    try:
        subject = subjectController.findOneSubject(subject_id)
        if subject is None:
            return jsonify({"error": f"Matéria {subject_id} não encontrada"}), 404
        return jsonify(subject)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subjects_bp.route("/subjects", methods=["POST"])
def create_subject():
    try:
        data = request.get_json()
        new_subject = subjectController.createSubject(data)
        return jsonify(new_subject), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subjects_bp.route("/subjects/<subject_id>", methods=["PUT"])
def update_subject(subject_id):
    try:
        data = request.get_json()
        success = subjectController.updateSubject(subject_id, data)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subjects_bp.route("/subjects/<subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    try:
        success = subjectController.deleteSubject(subject_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500