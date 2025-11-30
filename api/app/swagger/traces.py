from flask_restx import Namespace, Resource, fields

traces_ns = Namespace('traces', description='Operações com traces de atividades')

traces_model = traces_ns.model('Traces', {
    '_id': fields.String(readonly=True, description='ID do trace'),
    'lectureId': fields.String(required=True, description='ID da aula', example='lecture_123'),
    'onlineClass': fields.String(required=True, description='Classe online', example='Math Class'),
    'classTitle': fields.String(required=True, description='Título da classe', example='Advanced Mathematics'),
    'user': fields.String(required=True, description='Usuário', example='student123'),
    'url': fields.String(required=True, description='URL acessada', example='https://meet.google.com/abc-123'),
    'title': fields.String(required=True, description='Título da página', example='Google Meet'),
    'muted': fields.Boolean(required=True, description='Microfone silenciado', example=False),
    'cameraEnabled': fields.Boolean(required=True, description='Câmera habilitada', example=True),
    'microphoneEnabled': fields.Boolean(required=True, description='Microfone habilitado', example=True),
    'cameraStreaming': fields.Boolean(required=True, description='Câmera transmitindo', example=True),
    'microphoneStreaming': fields.Boolean(required=True, description='Microfone transmitindo', example=True),
    'lastAccessed': fields.String(required=True, description='Último acesso', example='2024-01-15T10:30:00Z'),
    'timestamp': fields.String(required=True, description='Timestamp do evento', example='2024-01-15T10:30:00Z'),
    'event': fields.String(required=True, description='Tipo de evento', example='tab_switch'),
    'lectureMuted': fields.Boolean(description='Aula silenciada', example=False),
    'lectureTabState': fields.String(description='Estado da aba da aula', example='active'),
    'lectureTabLastAccessed': fields.String(description='Último acesso da aba da aula', example='2024-01-15T10:30:00Z'),
    'lectureAudible': fields.Boolean(description='Aula audível', example=True),
    'lectureMutedInfoReason': fields.String(description='Motivo do silenciamento da aula', example='user_action')
})

traces_input_model = traces_ns.model('TracesInput', {
    'lectureId': fields.String(required=True, description='ID da aula', example='lecture_123'),
    'onlineClass': fields.String(required=True, description='Classe online', example='Math Class'),
    'classTitle': fields.String(required=True, description='Título da classe', example='Advanced Mathematics'),
    'user': fields.String(required=True, description='Usuário', example='student123'),
    'url': fields.String(required=True, description='URL acessada', example='https://meet.google.com/abc-123'),
    'title': fields.String(required=True, description='Título da página', example='Google Meet'),
    'muted': fields.Boolean(required=True, description='Microfone silenciado', example=False),
    'cameraEnabled': fields.Boolean(required=True, description='Câmera habilitada', example=True),
    'microphoneEnabled': fields.Boolean(required=True, description='Microfone habilitado', example=True),
    'cameraStreaming': fields.Boolean(required=True, description='Câmera transmitindo', example=True),
    'microphoneStreaming': fields.Boolean(required=True, description='Microfone transmitindo', example=True),
    'lastAccessed': fields.String(required=True, description='Último acesso', example='2024-01-15T10:30:00Z'),
    'timestamp': fields.String(required=True, description='Timestamp do evento', example='2024-01-15T10:30:00Z'),
    'event': fields.String(required=True, description='Tipo de evento', example='tab_switch'),
    'lectureMuted': fields.Boolean(description='Aula silenciada', example=False),
    'lectureTabState': fields.String(description='Estado da aba da aula', example='active'),
    'lectureTabLastAccessed': fields.String(description='Último acesso da aba da aula', example='2024-01-15T10:30:00Z'),
    'lectureAudible': fields.Boolean(description='Aula audível', example=True),
    'lectureMutedInfoReason': fields.String(description='Motivo do silenciamento da aula', example='user_action')
})

traces_update_model = traces_ns.model('TracesUpdate', {
    'lectureMuted': fields.Boolean(description='Aula silenciada', example=True),
    'lectureTabState': fields.String(description='Estado da aba da aula', example='inactive'),
    'lectureTabLastAccessed': fields.String(description='Último acesso da aba da aula', example='2024-01-15T11:30:00Z'),
    'lectureAudible': fields.Boolean(description='Aula audível', example=False),
    'lectureMutedInfoReason': fields.String(description='Motivo do silenciamento da aula', example='system_mute')
})

success_response_model = traces_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='Indica se a operação foi bem sucedida')
})

error_response_model = traces_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

def register_swagger_routes():
    """Registra as rotas Swagger para traces"""
    import app.controllers.traces as tracesController

    @traces_ns.route('/')
    class TracesList(Resource):
        @traces_ns.marshal_list_with(traces_model)
        @traces_ns.response(200, 'Lista de traces recuperada com sucesso')
        @traces_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Listar todos os traces"""
            try:
                return tracesController.findAllTraces()
            except Exception as e:
                traces_ns.abort(500, str(e))

        @traces_ns.expect(traces_input_model)
        @traces_ns.marshal_with(traces_model, code=201)
        @traces_ns.response(201, 'Trace criado com sucesso')
        @traces_ns.response(400, 'Dados de entrada inválidos')
        @traces_ns.response(500, 'Erro interno do servidor')
        def post(self):
            """Criar um novo trace"""
            try:
                data = traces_ns.payload
                new_trace = tracesController.createTrace(data)
                return new_trace, 201
            except Exception as e:
                traces_ns.abort(500, str(e))

    @traces_ns.route('/<string:trace_id>')
    @traces_ns.param('trace_id', 'ID do trace')
    class TraceDetail(Resource):
        @traces_ns.marshal_with(traces_model)
        @traces_ns.response(200, 'Trace encontrado')
        @traces_ns.response(404, 'Trace não encontrado')
        @traces_ns.response(500, 'Erro interno do servidor')
        def get(self, trace_id):
            """Obter trace por ID"""
            try:
                trace = tracesController.findOneTrace(trace_id)
                if trace is None:
                    traces_ns.abort(404, f'Trace {trace_id} não encontrado')
                return trace
            except Exception as e:
                traces_ns.abort(500, str(e))

        @traces_ns.expect(traces_update_model)
        @traces_ns.marshal_with(success_response_model)
        @traces_ns.response(200, 'Trace atualizado com sucesso')
        @traces_ns.response(404, 'Trace não encontrado')
        @traces_ns.response(500, 'Erro interno do servidor')
        def put(self, trace_id):
            """Atualizar trace existente"""
            try:
                data = traces_ns.payload
                success = tracesController.updateTrace(trace_id, data)
                return {'success': success}
            except Exception as e:
                traces_ns.abort(500, str(e))

        @traces_ns.marshal_with(success_response_model)
        @traces_ns.response(200, 'Trace deletado com sucesso')
        @traces_ns.response(404, 'Trace não encontrado')
        @traces_ns.response(500, 'Erro interno do servidor')
        def delete(self, trace_id):
            """Deletar trace"""
            try:
                success = tracesController.deleteTrace(trace_id)
                return {'success': success}
            except Exception as e:
                traces_ns.abort(500, str(e))

    @traces_ns.route('/lecture/<string:lecture_id>')
    @traces_ns.param('lecture_id', 'ID da aula')
    class TracesByLecture(Resource):
        @traces_ns.marshal_list_with(traces_model)
        @traces_ns.response(200, 'Traces da aula recuperados com sucesso')
        @traces_ns.response(404, 'Aula não encontrada')
        @traces_ns.response(500, 'Erro interno do servidor')
        def get(self, lecture_id):
            """Buscar traces por ID da aula"""
            try:
                traces = tracesController.findTracesByLecture(lecture_id)
                if not traces:
                    traces_ns.abort(404, f'Nenhum trace encontrado para a aula {lecture_id}')
                return traces
            except Exception as e:
                traces_ns.abort(500, str(e))

    return traces_ns