from flask import jsonify, Blueprint, request
import app.controllers.lectures as lectureController
from app.swagger.lectures import register_swagger_routes

lectures_bp = Blueprint("lectures", __name__)

lectures_ns = register_swagger_routes()


@lectures_bp.route("/lectures", methods=["GET"])
def findAllLectures():
    try:
        return jsonify(lectureController.findAllLectures()), 200
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500

@lectures_bp.route("/lectures", methods=["POST"])
def createLecture():
    try:
        data = request.get_json()
        lecture = lectureController.createLecture(data)
        return jsonify(lecture), 201
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500

@lectures_bp.route("/lectures/<_id>", methods=["GET"])
def findOneLecture(_id):
    try:
        return jsonify(lectureController.findOneLecture(_id))
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500

@lectures_bp.route("/lectures/subject/<subject_id>", methods=["GET"])
def getLecturesBySubject(subject_id):
    try:
        return jsonify(lectureController.findLecturesBySubject(subject_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lectures_bp.route("/lectures/<_id>", methods=["PUT"])
def updateLecture(_id):
    try:
        data = request.get_json()
        return jsonify(lectureController.updateLecture(_id, data))
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500

@lectures_bp.route("/lectures/<_id>", methods=["DELETE"])
def deleleteLecture(_id):
    try:
        return jsonify(lectureController.deleteLecture(_id))
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500