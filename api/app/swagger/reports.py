from flask_restx import Namespace, Resource, fields

# Criar namespace para relatórios
report_ns = Namespace('reports', description='Operações com relatórios de engajamento')

# Models para documentação Swagger
engagement_trend_model = report_ns.model('EngagementTrend', {
    'q1': fields.Float(description='Engajamento Q1'),
    'q2': fields.Float(description='Engajamento Q2'), 
    'q3': fields.Float(description='Engajamento Q3'),
    'q4': fields.Float(description='Engajamento Q4')
})

report_model = report_ns.model('Report', {
    '_id': fields.String(readonly=True, description='ID do relatório'),
    'lecture_id': fields.String(required=True, description='ID da aula'),
    'subject_id': fields.String(required=True, description='ID da disciplina'),
    'lecture_alias': fields.String(description='Apelido/Nome da aula'),
    'subject_name': fields.String(description='Nome da disciplina'),
    'teacher': fields.String(description='Professor'),
    'date_lecture': fields.String(description='Data da aula (DD/MM/YYYY)'),
    'total_students': fields.Integer(description='Total de estudantes'),
    
    'real_total_session_duration': fields.Float(description='Duração total real da sessão'),
    'avg_session_per_student': fields.Float(description='Tempo médio por estudante'),
    'attendance_ratio': fields.Float(description='Taxa de presença'),
    
    'lecture_focus_ratio': fields.Float(description='Taxa de foco na aula'),
    'avg_focus_duration': fields.Float(description='Duração média de foco'),
    'max_focus_duration': fields.Float(description='Duração máxima de foco'),
    
    'distraction_ratio': fields.Float(description='Taxa de distração'),
    'distraction_frequency': fields.Float(description='Frequência de distração'),
    'main_distractions': fields.List(fields.String, description='Principais distrações'),
    
    'tab_switch_frequency': fields.Float(description='Frequência de troca de abas'),
    'multitasking_intensity': fields.Float(description='Intensidade de multitarefa'),
    'focus_fragmentation': fields.Float(description='Fragmentação do foco'),
    
    'camera_engagement': fields.Float(description='Engajamento da câmera'),
    'mic_engagement': fields.Float(description='Engajamento do microfone'),
    'voluntary_participation': fields.Float(description='Participação voluntária'),
    
    'engagement_trend': fields.Nested(engagement_trend_model, description='Tendência de engajamento'),
    'peak_engagement_time': fields.String(description='Pico de engajamento'),
    'dropoff_point': fields.String(description='Ponto de queda de engajamento'),
    
    'engagement_score': fields.Float(description='Score geral de engajamento'),
    'attention_health': fields.Float(description='Saúde da atenção'),
    'distraction_risk': fields.Float(description='Risco de distração'),
    
    'issued_at': fields.String(readonly=True, description='Data de emissão')
})

report_input_model = report_ns.model('ReportInput', {
    'lecture_id': fields.String(required=True, description='ID da aula'),
    'subject_id': fields.String(required=True, description='ID da disciplina'),
    'lecture_alias': fields.String(description='Apelido/Nome da aula'),
    'subject_name': fields.String(description='Nome da disciplina'),
    'teacher': fields.String(description='Professor'),
    'date_lecture': fields.String(description='Data da aula (DD/MM/YYYY)'),
    'total_students': fields.Integer(description='Total de estudantes'),
    
    'real_total_session_duration': fields.Float(description='Duração total real da sessão'),
    'avg_session_per_student': fields.Float(description='Tempo médio por estudante'),
    'attendance_ratio': fields.Float(description='Taxa de presença'),
    
    'lecture_focus_ratio': fields.Float(description='Taxa de foco na aula'),
    'avg_focus_duration': fields.Float(description='Duração média de foco'),
    'max_focus_duration': fields.Float(description='Duração máxima de foco'),
    
    'distraction_ratio': fields.Float(description='Taxa de distração'),
    'distraction_frequency': fields.Float(description='Frequência de distração'),
    'main_distractions': fields.List(fields.String, description='Principais distrações'),
    
    'tab_switch_frequency': fields.Float(description='Frequência de troca de abas'),
    'multitasking_intensity': fields.Float(description='Intensidade de multitarefa'),
    'focus_fragmentation': fields.Float(description='Fragmentação do foco'),
    
    'camera_engagement': fields.Float(description='Engajamento da câmera'),
    'mic_engagement': fields.Float(description='Engajamento do microfone'),
    'voluntary_participation': fields.Float(description='Participação voluntária'),
    
    'engagement_trend': fields.Nested(engagement_trend_model, description='Tendência de engajamento'),
    'peak_engagement_time': fields.String(description='Pico de engajamento'),
    'dropoff_point': fields.String(description='Ponto de queda de engajamento'),
    
    'engagement_score': fields.Float(description='Score geral de engajamento'),
    'attention_health': fields.Float(description='Saúde da atenção'),
    'distraction_risk': fields.Float(description='Risco de distração')
})

def register_swagger_routes():
    """Registra as rotas Swagger no namespace"""
    from app.controllers import reports as reportController
    
    @report_ns.route('/')
    class ReportList(Resource):
        @report_ns.marshal_list_with(report_model)
        @report_ns.response(200, 'Lista de relatórios recuperada com sucesso')
        @report_ns.response(500, 'Erro interno do servidor')
        def get(self):
            """Listar todos os relatórios"""
            try:
                return reportController.findAllReports()
            except Exception as e:
                report_ns.abort(500, str(e))

        @report_ns.expect(report_input_model)
        @report_ns.marshal_with(report_model, code=201)
        @report_ns.response(201, 'Relatório criado com sucesso')
        @report_ns.response(400, 'Dados de entrada inválidos')
        @report_ns.response(500, 'Erro interno do servidor')
        def post(self):
            """Criar um novo relatório"""
            try:
                data = report_ns.payload
                return reportController.createReport(data), 201
            except Exception as e:
                report_ns.abort(500, str(e))

    @report_ns.route('/<string:report_id>')
    @report_ns.param('report_id', 'ID do relatório')
    class ReportDetail(Resource):
        @report_ns.marshal_with(report_model)
        @report_ns.response(200, 'Relatório encontrado')
        @report_ns.response(404, 'Relatório não encontrado')
        def get(self, report_id):
            """Obter relatório por ID"""
            try:
                result = reportController.findOneReport(report_id)
                if not result:
                    report_ns.abort(404, 'Relatório não encontrado')
                return result
            except Exception as e:
                report_ns.abort(404, str(e))

        @report_ns.expect(report_input_model)
        @report_ns.marshal_with(report_model)
        @report_ns.response(200, 'Relatório atualizado com sucesso')
        @report_ns.response(404, 'Relatório não encontrado')
        @report_ns.response(500, 'Erro interno do servidor')
        def put(self, report_id):
            """Atualizar relatório existente"""
            try:
                data = report_ns.payload
                result = reportController.updateReport(report_id, data)
                if not result:
                    report_ns.abort(404, 'Relatório não encontrado')
                return result
            except Exception as e:
                report_ns.abort(500, str(e))

        @report_ns.response(204, 'Relatório deletado com sucesso')
        @report_ns.response(404, 'Relatório não encontrado')
        @report_ns.response(500, 'Erro interno do servidor')
        def delete(self, report_id):
            """Deletar relatório"""
            try:
                result = reportController.deleteReport(report_id)
                if not result:
                    report_ns.abort(404, 'Relatório não encontrado')
                return '', 204
            except Exception as e:
                report_ns.abort(500, str(e))

    @report_ns.route('/pdf/<string:report_id>')
    @report_ns.param('report_id', 'ID do relatório')
    class ReportPDF(Resource):
        @report_ns.response(200, 'PDF gerado com sucesso')
        @report_ns.response(404, 'Relatório não encontrado')
        @report_ns.response(500, 'Erro ao gerar PDF')
        def get(self, report_id):
            """Gerar PDF do relatório"""
            try:
                return reportController.getReportPdf(report_id)
            except Exception as e:
                report_ns.abort(500, str(e))

    return report_ns