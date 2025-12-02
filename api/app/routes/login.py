from flask import jsonify, Blueprint, request
import app.controllers.login as loginController
import app.controllers.users as userController
from app.utils.logger import auth_logger, api_logger
from app.swagger.login import register_swagger_routes

login_bp = Blueprint("login", __name__)

login_ns = register_swagger_routes()

def resolve_user_id(email: str):
    """Busca o user_id a partir do email"""
    auth_logger.debug("Resolvendo user_id a partir do email", {'email': email})
    
    user = userController.findOneUser(email=email)
    if not user:
        auth_logger.warn("Usuário não encontrado", {'email': email})
        return None, f"Usuário {email} não encontrado"
    
    user_id = user.get("user_id") if isinstance(user, dict) else getattr(user, "user_id", None)
    auth_logger.debug("User_id resolvido com sucesso", {'email': email, 'user_id': user_id})
    return user_id, None


@login_bp.route("/login/token", methods=["PATCH"])
def patch_token():
    """Gera/atualiza o token do usuário"""
    try:
        email = request.args.get("email") or (request.get_json(silent=True) or {}).get("email")

        if not email:
            auth_logger.warn("Tentativa de gerar token sem email")
            return jsonify({"error": "email é obrigatório"}), 400

        auth_logger.info("Iniciando geração de token", {'email': email})

        user_id, err = resolve_user_id(email)
        if err:
            return jsonify({"error": err}), 404

        auth_logger.debug("Chamando updateToken", {'user_id': user_id, 'email': email})
        result = loginController.updateToken({"_id": user_id, "email": email})
        
        auth_logger.info("Token gerado com sucesso", {'email': email, 'user_id': user_id})
        return jsonify(result)
        
    except Exception as e:
        auth_logger.error("Erro ao gerar token", {
            'email': email,
            'error': str(e)
        })
        return jsonify({"error": str(e)}), 500

@login_bp.route("/login/token", methods=["GET"])
def get_token():
    """Valida se o token do usuário é válido"""
    try:
        email = request.args.get("email")
        user_token = request.args.get("token")

        if not email or not user_token:
            auth_logger.warn("Tentativa de validação sem email ou token", {
                'email_provided': bool(email),
                'token_provided': bool(user_token)
            })
            return jsonify({"error": "email e token são obrigatórios"}), 400

        auth_logger.info("Validando token", {'email': email})

        user_id, err = resolve_user_id(email)
        if err:
            return jsonify({"error": err}), 404

        result = loginController.getToken(user_id, user_token)
        
        if result:
            auth_logger.info("Token validado com sucesso", {'email': email, 'user_id': user_id})
        else:
            auth_logger.warn("Token inválido ou expirado", {'email': email, 'user_id': user_id})
            
        return jsonify(result)
        
    except Exception as e:
        auth_logger.error("Erro ao validar token", {
            'email': email,
            'error': str(e)
        })
        return jsonify({"error": str(e)}), 500