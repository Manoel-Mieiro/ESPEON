from flask import jsonify, Blueprint, request
import app.controllers.login as loginController
import app.controllers.users as userController

login_bp = Blueprint("login", __name__)


def resolve_user_id(email: str):
    """Busca o user_id a partir do email"""
    user = userController.findOneUser(email=email)
    if not user:
        return None, f"Usuário {email} não encontrado"
    
    user_id = user.get("user_id") if isinstance(user, dict) else getattr(user, "user_id", None)
    return user_id, None


@login_bp.route("/login/token", methods=["PATCH"])
def patch_token():
    """Gera/atualiza o token do usuário"""
    try:
        email = request.args.get("email") or (request.get_json(silent=True) or {}).get("email")

        if not email:
            return jsonify({"error": "email é obrigatório"}), 400

        user_id, err = resolve_user_id(email)
        if err:
            return jsonify({"error": err}), 404

        print("Chamando updateToken com:", user_id)
        return jsonify(loginController.updateToken({"_id": user_id, "email": email}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@login_bp.route("/login/token", methods=["GET"])
def get_token():
    """Valida se o token do usuário é válido"""
    try:
        email = request.args.get("email")
        user_token = request.args.get("token")

        if not email or not user_token:
            return jsonify({"error": "email e token são obrigatórios"}), 400

        user_id, err = resolve_user_id(email)
        if err:
            return jsonify({"error": err}), 404

        return jsonify(loginController.getToken(user_id, user_token))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
