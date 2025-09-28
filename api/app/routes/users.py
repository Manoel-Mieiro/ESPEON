from flask import jsonify, Blueprint, request
import app.controllers.users as userController

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        return jsonify(userController.findAllUsers()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        userController.createUser(data)
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import uuid

@users_bp.route("/users/<identifier>", methods=["GET"])
def findOneUser(identifier):
    try:
        user = None

        try:
            uuid_obj = uuid.UUID(identifier)
            user = userController.findOneUser(user_id=str(uuid_obj))
        except ValueError:
            user = userController.findOneUser(email=identifier)

        if user is None:
            return jsonify({"error": f"Usuário {identifier} não encontrado"}), 404

        return jsonify(user)

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        return jsonify(userController.updateUser(user_id, data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        return jsonify(userController.deleteUser(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
