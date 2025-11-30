from flask_restx import Namespace, Resource, fields

lectures_ns = Namespace('lectures', description='Operações com aulas/lectures')

lecture_model = lectures_ns.model('Lecture', {
    'lecture_id': fields.String(readonly=True, description='UUID da aula', example='123e4567-e89b-12d3-a456-426614174000'),
    'subject_id': fields.String(required=True, description='UUID da disciplina', example='123e4567-e89b-12d3-a456-426614174001'),
    'teacher_id': fields.String(required=True, description='UUID do professor', example='123e4567-e89b-12d3-a456-426614174002'),
    'date_lecture': fields.String(required=True, description='Data da aula (YYYY-MM-DD)', example='2024-01-15'),
    'period_start': fields.String(required=True, description='Horário de início (HH:MM:SS)', example='09:00:00'),
    'period_end': fields.String(required=True, description='Horário de término (HH:MM:SS)', example='11:00:00')
})

lecture_input_model = lectures_ns.model('LectureInput', {
    'subject_id': fields.String(required=True, description='UUID da disciplina', example='123e4567-e89b-12d3-a456-426614174001'),
    'teacher_id': fields.String(required=True, description='UUID do professor', example='123e4567-e89b-12d3-a456-426614174002'),
    'date_lecture': fields.String(required=True, description='Data da aula (YYYY-MM-DD)', example='2024-01-15'),
    'period_start': fields.String(required=True, description='Horário de início (HH:MM:SS)', example='09:00:00'),
    'period_end': fields.String(required=True, description='Horário de término (HH:MM:SS)', example='11:00:00'),
    'lecture_id': fields.String(description='UUID da aula (opcional, será gerado se não fornecido)', example='123e4567-e89b-12d3-a456-426614174000')
})

lecture_update_model = lectures_ns.model('LectureUpdate', {
    'subject_id': fields.String(description='UUID da disciplina', example='123e4567-e89b-12d3-a456-426614174001'),
    'teacher_id': fields.String(description='UUID do professor', example='123e4567-e89b-12d3-a456-426614174002'),
    'date_lecture': fields.String(description='Data da aula (YYYY-MM-DD)', example='2024-01-15'),
    'period_start': fields.String(description='Horário de início (HH:MM:SS)', example='09:00:00'),
    'period_end': fields.String(description='Horário de término (HH:MM:SS)', example='11:00:00')
})

success_response_model = lectures_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='Indica se a operação foi bem sucedida')
})

error_response_model = lectures_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

def register_swagger_routes():
    """Registra as rotas Swagger para lectures"""
    import app.controllers.lectures as lectureController

    @lectures_ns.route('/')
    class LectureList(Resource):
        @lectures_ns.marshal_list_with(lecture_model)
        @lectures_ns.response(200, 'Lista de aulas recuperada com sucesso')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Listar todas as aulas"""
            try:
                return lectureController.findAllLectures()
            except Exception as e:
                lectures_ns.abort(500, str(e))

        @lectures_ns.expect(lecture_input_model)
        @lectures_ns.marshal_with(lecture_model, code=201)
        @lectures_ns.response(201, 'Aula criada com sucesso')
        @lectures_ns.response(400, 'Dados de entrada inválidos')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def post(self):
            """Criar uma nova aula"""
            try:
                data = lectures_ns.payload
                lecture = lectureController.createLecture(data)
                return lecture, 201
            except Exception as e:
                lectures_ns.abort(500, str(e))

    @lectures_ns.route('/<string:lecture_id>')
    @lectures_ns.param('lecture_id', 'UUID da aula')
    class LectureDetail(Resource):
        @lectures_ns.marshal_with(lecture_model)
        @lectures_ns.response(200, 'Aula encontrada')
        @lectures_ns.response(404, 'Aula não encontrada')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def get(self, lecture_id):
            """Obter aula por ID"""
            try:
                lecture = lectureController.findOneLecture(lecture_id)
                if not lecture:
                    lectures_ns.abort(404, f'Aula {lecture_id} não encontrada')
                return lecture
            except Exception as e:
                lectures_ns.abort(500, str(e))

        @lectures_ns.expect(lecture_update_model)
        @lectures_ns.marshal_with(lecture_model)
        @lectures_ns.response(200, 'Aula atualizada com sucesso')
        @lectures_ns.response(404, 'Aula não encontrada')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def put(self, lecture_id):
            """Atualizar aula existente"""
            try:
                data = lectures_ns.payload
                result = lectureController.updateLecture(lecture_id, data)
                if not result:
                    lectures_ns.abort(404, f'Aula {lecture_id} não encontrada')
                return result
            except Exception as e:
                lectures_ns.abort(500, str(e))

        @lectures_ns.marshal_with(success_response_model)
        @lectures_ns.response(200, 'Aula deletada com sucesso')
        @lectures_ns.response(404, 'Aula não encontrada')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def delete(self, lecture_id):
            """Deletar aula"""
            try:
                result = lectureController.deleteLecture(lecture_id)
                if not result:
                    lectures_ns.abort(404, f'Aula {lecture_id} não encontrada')
                return {'success': True}
            except Exception as e:
                lectures_ns.abort(500, str(e))

    @lectures_ns.route('/subject/<string:subject_id>')
    @lectures_ns.param('subject_id', 'UUID da disciplina')
    class LecturesBySubject(Resource):
        @lectures_ns.marshal_list_with(lecture_model)
        @lectures_ns.response(200, 'Aulas da disciplina recuperadas com sucesso')
        @lectures_ns.response(404, 'Disciplina não encontrada ou sem aulas')
        @lectures_ns.response(500, 'Erro interno do servidor')
        def get(self, subject_id):
            """Buscar aulas por disciplina"""
            try:
                lectures = lectureController.findLecturesBySubject(subject_id)
                if not lectures:
                    lectures_ns.abort(404, f'Nenhuma aula encontrada para a disciplina {subject_id}')
                return lectures
            except Exception as e:
                lectures_ns.abort(500, str(e))

    return lectures_ns