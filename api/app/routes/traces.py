from flask import Blueprint, request, jsonify
from app.controllers import traces as tracesController
from app.swagger.traces import register_swagger_routes

traces_bp = Blueprint("traces_bp", __name__, url_prefix="/traces")

traces_ns = register_swagger_routes()


@traces_bp.route("/", methods=["GET"])
def get_all_traces():
    try:
        return jsonify(tracesController.findAllTraces()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traces_bp.route("/", methods=["POST"])
def create_trace():
    try:
        data = request.get_json()
        return jsonify(tracesController.createTrace(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traces_bp.route("/<trace_id>", methods=["GET"])
def get_trace(trace_id):
    try:
        trace = tracesController.findOneTrace(trace_id)
        if trace is None:
            return jsonify({"error": f"Trace {trace_id} não encontrado"}), 404
        return jsonify(trace)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traces_bp.route("/<trace_id>", methods=["PUT"])
def update_trace(trace_id):
    try:
        data = request.get_json()
        success = tracesController.updateTrace(trace_id, data)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traces_bp.route("/<trace_id>", methods=["DELETE"])
def delete_trace(trace_id):
    try:
        success = tracesController.deleteTrace(trace_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota adicional para buscar por lecture_id
@traces_bp.route("/lecture/<lecture_id>", methods=["GET"])
def get_traces_by_lecture(lecture_id):
    try:
        traces = tracesController.findTracesByLecture(lecture_id)
        if not traces:
            return jsonify({"error": f"Nenhum trace encontrado para a aula {lecture_id}"}), 404
        return jsonify(traces)
    except Exception as e:
        return jsonify({"error": str(e)}), 500