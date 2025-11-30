from flask_restx import Namespace, Resource, fields

subjects_ns = Namespace('subjects', description='Operações com matérias/disciplinas')

subject_model = subjects_ns.model('Subject', {
    'subject_id': fields.String(readonly=True, description='UUID da disciplina'),
    'name': fields.String(required=True, description='Nome da disciplina', example='Matemática')
})

subject_input_model = subjects_ns.model('SubjectInput', {
    'name': fields.String(required=True, description='Nome da disciplina', example='Matemática'),
    'subject_id': fields.String(description='UUID da disciplina (opcional)')
})

subject_update_model = subjects_ns.model('SubjectUpdate', {
    'name': fields.String(description='Nome da disciplina', example='Matemática Atualizada')
})

success_response_model = subjects_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='Indica se a operação foi bem sucedida')
})

error_response_model = subjects_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

def register_swagger_routes():
    """Registra as rotas Swagger para subjects"""
    import app.controllers.subject as subjectController

    @subjects_ns.route('/')
    class SubjectList(Resource):
        @subjects_ns.marshal_list_with(subject_model)
        @subjects_ns.response(200, 'Lista de disciplinas recuperada com sucesso')
        @subjects_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Listar todas as disciplinas"""
            try:
                return subjectController.findAllSubjects()
            except Exception as e:
                subjects_ns.abort(500, str(e))

        @subjects_ns.expect(subject_input_model)
        @subjects_ns.marshal_with(subject_model, code=201)
        @subjects_ns.response(201, 'Disciplina criada com sucesso')
        @subjects_ns.response(400, 'Dados de entrada inválidos')
        @subjects_ns.response(500, 'Erro interno do servidor')
        def post(self):
            """Criar uma nova disciplina"""
            try:
                data = subjects_ns.payload
                new_subject = subjectController.createSubject(data)
                return new_subject, 201
            except Exception as e:
                subjects_ns.abort(500, str(e))

    @subjects_ns.route('/<string:subject_id>')
    @subjects_ns.param('subject_id', 'UUID da disciplina')
    class SubjectDetail(Resource):
        @subjects_ns.marshal_with(subject_model)
        @subjects_ns.response(200, 'Disciplina encontrada')
        @subjects_ns.response(404, 'Disciplina não encontrada')
        @subjects_ns.response(500, 'Erro interno do servidor')
        def get(self, subject_id):
            """Obter disciplina por ID"""
            try:
                subject = subjectController.findOneSubject(subject_id)
                if subject is None:
                    subjects_ns.abort(404, f'Disciplina {subject_id} não encontrada')
                return subject
            except Exception as e:
                subjects_ns.abort(500, str(e))

        @subjects_ns.expect(subject_update_model)
        @subjects_ns.marshal_with(success_response_model)
        @subjects_ns.response(200, 'Disciplina atualizada com sucesso')
        @subjects_ns.response(404, 'Disciplina não encontrada')
        @subjects_ns.response(500, 'Erro interno do servidor')
        def put(self, subject_id):
            """Atualizar disciplina existente"""
            try:
                data = subjects_ns.payload
                success = subjectController.updateSubject(subject_id, data)
                return {'success': success}
            except Exception as e:
                subjects_ns.abort(500, str(e))

        @subjects_ns.marshal_with(success_response_model)
        @subjects_ns.response(200, 'Disciplina deletada com sucesso')
        @subjects_ns.response(404, 'Disciplina não encontrada')
        @subjects_ns.response(500, 'Erro interno do servidor')
        def delete(self, subject_id):
            """Deletar disciplina"""
            try:
                success = subjectController.deleteSubject(subject_id)
                return {'success': success}
            except Exception as e:
                subjects_ns.abort(500, str(e))

    return subjects_ns