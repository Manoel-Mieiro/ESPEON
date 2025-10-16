from app.models.postgres.reports_student import ReportStudent


class ReportStudentDTO:
    def __init__(
        self,
        report_id: str,
        user_id: str,
        total_time_watched: float = None,
        attention_span: float = None,
        cam_enabled: bool = None,
        mic_enabled: bool = None,
        cam_streaming_span: float = None,
        mic_streaming_span: float = None
    ):
        """
        :param report_id: UUID do relatório agregado (Report)
        :param user_id: UUID do usuário (aluno)
        :param total_time_watched: Tempo total assistido pelo aluno (minutos)
        :param attention_span: Percentual médio de atenção do aluno
        :param cam_enabled: Se o aluno manteve a câmera ligada
        :param mic_enabled: Se o aluno manteve o microfone ligado
        :param cam_streaming_span: Tempo total de transmissão de câmera
        :param mic_streaming_span: Tempo total de transmissão de microfone
        """
        if not report_id or not user_id:
            raise ValueError("report_id and user_id are required")

        self.report_id = report_id
        self.user_id = user_id
        self.total_time_watched = total_time_watched
        self.attention_span = attention_span
        self.cam_enabled = cam_enabled
        self.mic_enabled = mic_enabled
        self.cam_streaming_span = cam_streaming_span
        self.mic_streaming_span = mic_streaming_span

    def to_standard(self):
        """
        Converte para o modelo ReportStudent do Postgres
        """
        return ReportStudent(
            report_id=self.report_id,
            user_id=self.user_id,
            total_time_watched=self.total_time_watched,
            attention_span=self.attention_span,
            cam_enabled=self.cam_enabled,
            mic_enabled=self.mic_enabled,
            cam_streaming_span=self.cam_streaming_span,
            mic_streaming_span=self.mic_streaming_span
        )
