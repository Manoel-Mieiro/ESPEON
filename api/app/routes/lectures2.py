from flask import jsonify, Blueprint, request
import app.controllers.lectures2 as lectureController

lectures2_bp = Blueprint("lectures2", __name__)

@lectures2_bp.route("/lectures2", methods=["GET"])
def findAllLectures():
    try:
        return jsonify(lectureController.findAllLectures()), 200
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500
