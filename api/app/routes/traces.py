from flask import jsonify, Blueprint, request
import app.controllers.traces as traceController

traces_bp = Blueprint("traces", __name__)


@traces_bp.route("/traces/", methods=["GET"])
def listTraces():
    try:
        traces = traceController.listTraces()
        if traces:
            return jsonify(traces), 200
        else:
            return jsonify([]), 204
    except Exception as e:
        return jsonify({"error": f"[ROUTES] {str(e)}"}), 500

@traces_bp.route("/traces/<lecture_id>", methods=["GET"])
def findOneTraceByLecture(lecture_id):
    try:
        traces = traceController.findOneTraceByLecture(lecture_id)
        if traces:
            return jsonify(traces), 200
        else:
            return jsonify([]), 204
    except Exception as e:
        return jsonify({"error": f"[ROUTES] {str(e)}"}), 500

@traces_bp.route("/traces", methods=["POST"])
def createTrace():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        new_trace = traceController.createTrace(data)
        return jsonify(new_trace), 201
    except Exception as e:
        return jsonify({"[ROUTES]error": str(e)}), 500
