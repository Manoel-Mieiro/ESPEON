from app.utils.time_utils import get_current_datetime
from app.models.postgres.reports import Report
from datetime import datetime, timedelta


class ReportDTO:
    def __init__(
        self,
        lecture_id: str,
        subject_id: str,
        total_students: int = 0,

        real_total_session_duration: float = None,
        avg_session_per_student: float = None,
        attendance_ratio: float = None,

        lecture_focus_ratio: float = None,
        avg_focus_duration: float = None,
        max_focus_duration: float = None,

        distraction_ratio: float = None,
        distraction_frequency: float = None,
        main_distractions: list = None,

        tab_switch_frequency: float = None,
        multitasking_intensity: float = None,
        focus_fragmentation: float = None,

        camera_engagement: float = None,
        mic_engagement: float = None,
        voluntary_participation: float = None,

        engagement_trend: dict = None,
        peak_engagement_time: str = None,
        dropoff_point: str = None,

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

        self.real_total_session_duration = real_total_session_duration
        self.avg_session_per_student = avg_session_per_student
        self.attendance_ratio = attendance_ratio

        self.lecture_focus_ratio = lecture_focus_ratio
        self.avg_focus_duration = avg_focus_duration
        self.max_focus_duration = max_focus_duration

        self.distraction_ratio = distraction_ratio
        self.distraction_frequency = distraction_frequency
        self.main_distractions = main_distractions

        self.tab_switch_frequency = tab_switch_frequency
        self.multitasking_intensity = multitasking_intensity
        self.focus_fragmentation = focus_fragmentation

        self.camera_engagement = camera_engagement
        self.mic_engagement = mic_engagement
        self.voluntary_participation = voluntary_participation

        self.engagement_trend = engagement_trend or {
            "q1": 0.0,
            "q2": 0.0,
            "q3": 0.0,
            "q4": 0.0
        }
        self.peak_engagement_time = peak_engagement_time
        self.dropoff_point = dropoff_point

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

            real_total_session_duration=self.real_total_session_duration,
            avg_session_per_student=self.avg_session_per_student,
            attendance_ratio=self.attendance_ratio,

            lecture_focus_ratio=self.lecture_focus_ratio,
            avg_focus_duration=self.avg_focus_duration,
            max_focus_duration=self.max_focus_duration,

            distraction_ratio=self.distraction_ratio,
            distraction_frequency=self.distraction_frequency,
            main_distractions=self.main_distractions,

            tab_switch_frequency=self.tab_switch_frequency,
            multitasking_intensity=self.multitasking_intensity,
            focus_fragmentation=self.focus_fragmentation,

            camera_engagement=self.camera_engagement,
            mic_engagement=self.mic_engagement,
            voluntary_participation=self.voluntary_participation,

            engagement_trend=self.engagement_trend,
            peak_engagement_time=self.peak_engagement_time,
            dropoff_point=self.dropoff_point,

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
