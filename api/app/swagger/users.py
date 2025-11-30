from flask_restx import Namespace, Resource, fields
from enum import Enum

users_ns = Namespace('users', description='Operações com usuários')

roles_enum = users_ns.model('Roles', {
    'ADMIN': fields.String(description='Administrador'),
    'EDUCATOR': fields.String(description='Educador/Professor'),
    'STUDENT': fields.String(description='Estudante')
})

user_model = users_ns.model('User', {
    'user_id': fields.String(readonly=True, description='UUID do usuário', example='123e4567-e89b-12d3-a456-426614174000'),
    'email': fields.String(required=True, description='Email do usuário', example='usuario@example.com'),
    'role': fields.String(required=True, description='Papel do usuário', enum=['admin', 'educator', 'student'], example='student')
})

user_input_model = users_ns.model('UserInput', {
    'email': fields.String(required=True, description='Email do usuário', example='usuario@example.com'),
    'role': fields.String(required=True, description='Papel do usuário', enum=['admin', 'educator', 'student'], example='student'),
    'user_id': fields.String(description='UUID do usuário (opcional)', example='123e4567-e89b-12d3-a456-426614174000')
})

user_update_model = users_ns.model('UserUpdate', {
    'email': fields.String(description='Email do usuário', example='novo_email@example.com'),
    'role': fields.String(description='Papel do usuário', enum=['admin', 'educator', 'student'], example='educator')
})

success_response_model = users_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='Indica se a operação foi bem sucedida')
})

message_response_model = users_ns.model('MessageResponse', {
    'message': fields.String(description='Mensagem de sucesso')
})

error_response_model = users_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

def register_swagger_routes():
    """Registra as rotas Swagger para users"""
    import app.controllers.users as userController
    import uuid

    @users_ns.route('/')
    class UserList(Resource):
        @users_ns.marshal_list_with(user_model)
        @users_ns.response(200, 'Lista de usuários recuperada com sucesso')
        @users_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Listar todos os usuários"""
            try:
                return userController.findAllUsers()
            except Exception as e:
                users_ns.abort(500, str(e))

        @users_ns.expect(user_input_model)
        @users_ns.marshal_with(message_response_model, code=201)
        @users_ns.response(201, 'Usuário criado com sucesso')
        @users_ns.response(400, 'Dados de entrada inválidos')
        @users_ns.response(500, 'Erro interno do servidor')
        def post(self):
            """Criar um novo usuário"""
            try:
                data = users_ns.payload
                userController.createUser(data)
                return {'message': 'Usuário cadastrado com sucesso'}, 201
            except Exception as e:
                users_ns.abort(500, str(e))

    @users_ns.route('/<string:identifier>')
    @users_ns.param('identifier', 'UUID do usuário ou email')
    class UserDetail(Resource):
        @users_ns.marshal_with(user_model)
        @users_ns.response(200, 'Usuário encontrado')
        @users_ns.response(404, 'Usuário não encontrado')
        @users_ns.response(500, 'Erro interno do servidor')
        def get(self, identifier):
            """Obter usuário por UUID ou email"""
            try:
                user = None

                try:
                    uuid_obj = uuid.UUID(identifier)
                    user = userController.findOneUser(user_id=str(uuid_obj))
                except ValueError:
                    user = userController.findOneUser(email=identifier)

                if user is None:
                    users_ns.abort(404, f'Usuário {identifier} não encontrado')

                return user

            except Exception as e:
                users_ns.abort(500, str(e))

        @users_ns.expect(user_update_model)
        @users_ns.marshal_with(user_model)
        @users_ns.response(200, 'Usuário atualizado com sucesso')
        @users_ns.response(404, 'Usuário não encontrado')
        @users_ns.response(500, 'Erro interno do servidor')
        def put(self, identifier):
            """Atualizar usuário existente"""
            try:
                data = users_ns.payload
                
                user = None
                try:
                    uuid_obj = uuid.UUID(identifier)
                    user = userController.findOneUser(user_id=str(uuid_obj))
                except ValueError:
                    user = userController.findOneUser(email=identifier)

                if user is None:
                    users_ns.abort(404, f'Usuário {identifier} não encontrado')

                user_id = user.get('user_id') if isinstance(user, dict) else getattr(user, 'user_id', None)
                if not user_id:
                    users_ns.abort(404, f'ID do usuário não encontrado')

                result = userController.updateUser(user_id, data)
                return result

            except Exception as e:
                users_ns.abort(500, str(e))

        @users_ns.marshal_with(success_response_model)
        @users_ns.response(200, 'Usuário deletado com sucesso')
        @users_ns.response(404, 'Usuário não encontrado')
        @users_ns.response(500, 'Erro interno do servidor')
        def delete(self, identifier):
            """Deletar usuário"""
            try:
                user = None
                try:
                    uuid_obj = uuid.UUID(identifier)
                    user = userController.findOneUser(user_id=str(uuid_obj))
                except ValueError:
                    user = userController.findOneUser(email=identifier)

                if user is None:
                    users_ns.abort(404, f'Usuário {identifier} não encontrado')

                user_id = user.get('user_id') if isinstance(user, dict) else getattr(user, 'user_id', None)
                if not user_id:
                    users_ns.abort(404, f'ID do usuário não encontrado')

                result = userController.deleteUser(user_id)
                return {'success': True}

            except Exception as e:
                users_ns.abort(500, str(e))

    return users_ns