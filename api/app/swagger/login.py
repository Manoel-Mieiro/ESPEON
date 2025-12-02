from flask_restx import Namespace, Resource, fields

login_ns = Namespace('auth', description='Operações de autenticação e tokens')

token_generate_model = login_ns.model('TokenGenerateInput', {
    'email': fields.String(required=True, description='Email do usuário', example='usuario@example.com')
})

token_validate_model = login_ns.model('TokenValidateInput', {
    'email': fields.String(required=True, description='Email do usuário', example='usuario@example.com'),
    'token': fields.String(required=True, description='Token para validação', example='abc123-token')
})

token_response_model = login_ns.model('TokenResponse', {
    'token': fields.String(description='Token gerado/validado'),
    'expires_at': fields.String(description='Data de expiração do token'),
    'user_id': fields.String(description='ID do usuário'),
    'email': fields.String(description='Email do usuário')
})

token_validation_response_model = login_ns.model('TokenValidationResponse', {
    'valid': fields.Boolean(description='Indica se o token é válido'),
    'user_id': fields.String(description='ID do usuário'),
    'email': fields.String(description='Email do usuário'),
    'expires_at': fields.String(description='Data de expiração do token')
})

error_response_model = login_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

def register_swagger_routes():
    """Registra as rotas Swagger para login"""
    import app.controllers.login as loginController
    import app.controllers.users as userController
    from app.utils.logger import auth_logger
    
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

    @login_ns.route('/token')
    class TokenManagement(Resource):
        @login_ns.expect(token_generate_model)
        @login_ns.marshal_with(token_response_model, code=200)
        @login_ns.response(200, 'Token gerado/atualizado com sucesso')
        @login_ns.response(400, 'Email é obrigatório')
        @login_ns.response(404, 'Usuário não encontrado')
        @login_ns.response(500, 'Erro interno do servidor')
        def patch(self):
            """Gerar/atualizar token do usuário"""
            try:
                email = login_ns.payload.get('email') if login_ns.payload else None
                
                if not email:
                    auth_logger.warn("Tentativa de gerar token sem email")
                    login_ns.abort(400, 'email é obrigatório')

                auth_logger.info("Iniciando geração de token", {'email': email})

                user_id, err = resolve_user_id(email)
                if err:
                    login_ns.abort(404, err)

                auth_logger.debug("Chamando updateToken", {'user_id': user_id, 'email': email})
                result = loginController.updateToken({"_id": user_id, "email": email})
                
                auth_logger.info("Token gerado com sucesso", {'email': email, 'user_id': user_id})
                return result
                
            except Exception as e:
                auth_logger.error("Erro ao gerar token", {
                    'email': email,
                    'error': str(e)
                })
                login_ns.abort(500, str(e))

        @login_ns.doc(params={
            'email': {'description': 'Email do usuário', 'required': True, 'type': 'string'},
            'token': {'description': 'Token para validação', 'required': True, 'type': 'string'}
        })
        @login_ns.marshal_with(token_validation_response_model, code=200)
        @login_ns.response(200, 'Token validado com sucesso')
        @login_ns.response(400, 'Email e token são obrigatórios')
        @login_ns.response(404, 'Usuário não encontrado')
        @login_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Validar token do usuário"""
            try:
                email = login_ns.payload.get('email') if hasattr(login_ns, 'payload') and login_ns.payload else None
                user_token = login_ns.payload.get('token') if hasattr(login_ns, 'payload') and login_ns.payload else None
                
                from flask import request
                if not email:
                    email = request.args.get('email')
                if not user_token:
                    user_token = request.args.get('token')

                if not email or not user_token:
                    auth_logger.warn("Tentativa de validação sem email ou token", {
                        'email_provided': bool(email),
                        'token_provided': bool(user_token)
                    })
                    login_ns.abort(400, 'email e token são obrigatórios')

                auth_logger.info("Validando token", {'email': email})

                user_id, err = resolve_user_id(email)
                if err:
                    login_ns.abort(404, err)

                result = loginController.getToken(user_id, user_token)
                
                if result:
                    auth_logger.info("Token validado com sucesso", {'email': email, 'user_id': user_id})
                else:
                    auth_logger.warn("Token inválido ou expirado", {'email': email, 'user_id': user_id})
                    
                return result
                
            except Exception as e:
                auth_logger.error("Erro ao validar token", {
                    'email': email,
                    'error': str(e)
                })
                login_ns.abort(500, str(e))

    return login_ns