from flask import jsonify, Blueprint, request
import app.controllers.subject as subjectController

subjects_bp = Blueprint("subjects", __name__)


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
        subjectController.createSubject(data)
        return jsonify({"message": "Matéria cadastrada com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@subjects_bp.route("/subjects/<subject_id>", methods=["PUT"])
def update_subject(subject_id):
    try:
        data = request.get_json()
        return jsonify(subjectController.updateSubject(subject_id, data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@subjects_bp.route("/subjects/<subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    try:
        return jsonify(subjectController.deleteSubject(subject_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
