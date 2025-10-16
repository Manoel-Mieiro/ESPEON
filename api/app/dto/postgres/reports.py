from app.models.postgres.reports import Report
from datetime import datetime, timedelta

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

        # Ajusta issued_at para fuso horário de Brasília
        if isinstance(issued_at, str):
            dt = datetime.strptime(issued_at, "%Y-%m-%d %H:%M:%S")
            self.issued_at = dt - timedelta(hours=3)  # subtrai 3h para GMT-3
        elif isinstance(issued_at, datetime):
            self.issued_at = issued_at - timedelta(hours=3)
        else:
            self.issued_at = datetime.utcnow() - timedelta(hours=3)

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
