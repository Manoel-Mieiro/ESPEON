from app.models.postgres.reports import Report
from datetime import datetime


class ReportDTO:
    def __init__(
        self,
        lecture_id: str,
        subject_id: str,
        total_students: int = 0,
        total_time_watched: float = 0.0,
        avg_lecture_duration: float = None,
        avg_idle_duration: float = None,
        avg_attention_span: float = None,
        pct_enabled_camera: float = None,
        pct_enabled_mic: float = None,
        avg_cam_streaming_span: float = None,
        avg_mic_streaming_span: float = None,
        issued_at: str = None
    ):
        """
        :param lecture_id: UUID da aula
        :param subject_id: UUID da disciplina
        :param total_students: Total de alunos participantes
        :param total_time_watched: Tempo total assistido (minutos)
        :param avg_lecture_duration: Duração média da aula (minutos)
        :param avg_idle_duration: Duração média de inatividade (minutos)
        :param avg_attention_span: Média de atenção dos alunos (%)
        :param pct_enabled_camera: Percentual médio de câmeras ligadas (%)
        :param pct_enabled_mic: Percentual médio de microfones ligados (%)
        :param avg_cam_streaming_span: Duração média do streaming de câmera (minutos)
        :param avg_mic_streaming_span: Duração média do streaming de microfone (minutos)
        :param issued_at: Data/hora de emissão no formato 'YYYY-MM-DD HH:MM:SS' (opcional)
        """
        if not lecture_id or not subject_id:
            raise ValueError("lecture_id and subject_id are required")

        self.lecture_id = lecture_id
        self.subject_id = subject_id
        self.total_students = total_students
        self.total_time_watched = total_time_watched
        self.avg_lecture_duration = avg_lecture_duration
        self.avg_idle_duration = avg_idle_duration
        self.avg_attention_span = avg_attention_span
        self.pct_enabled_camera = pct_enabled_camera
        self.pct_enabled_mic = pct_enabled_mic
        self.avg_cam_streaming_span = avg_cam_streaming_span
        self.avg_mic_streaming_span = avg_mic_streaming_span

        self.issued_at = (
            datetime.strptime(
                issued_at, "%Y-%m-%d %H:%M:%S") if issued_at else datetime.utcnow()
        )

    def to_standard(self):
        """
        Converte para o modelo Report do Postgres
        """
        return Report(
            lecture_id=self.lecture_id,
            subject_id=self.subject_id,
            total_students=self.total_students,
            total_time_watched=self.total_time_watched,
            avg_lecture_duration=self.avg_lecture_duration,
            avg_idle_duration=self.avg_idle_duration,
            avg_attention_span=self.avg_attention_span,
            pct_enabled_camera=self.pct_enabled_camera,
            pct_enabled_mic=self.pct_enabled_mic,
            avg_cam_streaming_span=self.avg_cam_streaming_span,
            avg_mic_streaming_span=self.avg_mic_streaming_span,
            issued_at=self.issued_at
        )
