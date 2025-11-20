from app.utils.time_utils import get_current_datetime
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
        min_lecture_duration: float = None,
        max_lecture_duration: float = None,
        min_idle_duration: float = None,
        max_idle_duration: float = None,
        min_attention_span: float = None,
        max_attention_span: float = None,
        issued_at: str = None
    ):
        """
        :param lecture_id: UUID da aula
        :param subject_id: UUID da disciplina
        :param total_students: Total de alunos participantes
        :param total_time_watched: Tempo total assistido (minutos)
        :param avg_lecture_duration: Duração média das aulas da disciplina (minutos)
        :param avg_idle_duration: Tempo médio ocioso dos alunos (minutos)
        :param avg_attention_span: Tempo médio de atenção dos alunos (minutos)
        :param pct_enabled_camera: Percentual médio de câmeras ligadas (%)
        :param pct_enabled_mic: Percentual médio de microfones ligados (%)
        :param avg_cam_streaming_span: Duração média do streaming de câmera (minutos)
        :param avg_mic_streaming_span: Duração média do streaming de microfone (minutos)
        :param min_lecture_duration: Menor duração registrada de aula (minutos)
        :param max_lecture_duration: Maior duração registrada de aula (minutos)
        :param min_idle_duration: Menor tempo ocioso registrado (minutos)
        :param max_idle_duration: Maior tempo ocioso registrado (minutos)
        :param min_attention_span: Menor tempo médio de atenção (minutos)
        :param max_attention_span: Maior tempo médio de atenção (minutos)
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
        self.min_lecture_duration = min_lecture_duration
        self.max_lecture_duration = max_lecture_duration
        self.min_idle_duration = min_idle_duration
        self.max_idle_duration = max_idle_duration
        self.min_attention_span = min_attention_span
        self.max_attention_span = max_attention_span

        self.issued_at = (
            datetime.strptime(
                issued_at, "%Y-%m-%d %H:%M:%S") if issued_at else get_current_datetime()
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
            min_lecture_duration=self.min_lecture_duration,
            max_lecture_duration=self.max_lecture_duration,
            min_idle_duration=self.min_idle_duration,
            max_idle_duration=self.max_idle_duration,
            min_attention_span=self.min_attention_span,
            max_attention_span=self.max_attention_span,
            issued_at=self.issued_at
        )
