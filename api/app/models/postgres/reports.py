from bson import ObjectId
from datetime import datetime
from app.utils.time_utils import get_current_datetime

class Report:
    def __init__(
        self,
        lecture_id: str,
        subject_id: str,
        lecture_alias: str = None,
        subject_name: str = None,
        teacher: str = None,
        date_lecture: datetime = None,
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
        issued_at: datetime = None,
        _id: ObjectId = None
    ):
        self._id = _id
        self._lecture_id = lecture_id
        self._subject_id = subject_id
        self._lecture_alias = lecture_alias
        self._subject_name = subject_name
        self._teacher = teacher
        self._date_lecture = date_lecture or datetime.utcnow()
        self._total_students = total_students


        self._real_total_session_duration = real_total_session_duration
        self._avg_session_per_student = avg_session_per_student
        self._attendance_ratio = attendance_ratio


        self._lecture_focus_ratio = lecture_focus_ratio
        self._avg_focus_duration = avg_focus_duration
        self._max_focus_duration = max_focus_duration

        self._distraction_ratio = distraction_ratio
        self._distraction_frequency = distraction_frequency
        self._main_distractions = main_distractions

        self._total_time_watched = total_time_watched
        self._avg_lecture_duration = avg_lecture_duration
        self._avg_idle_duration = avg_idle_duration
        self._avg_attention_span = avg_attention_span
        self._pct_enabled_camera = pct_enabled_camera
        self._pct_enabled_mic = pct_enabled_mic
        self._avg_cam_streaming_span = avg_cam_streaming_span
        self._avg_mic_streaming_span = avg_mic_streaming_span
        self._min_lecture_duration = min_lecture_duration
        self._max_lecture_duration = max_lecture_duration
        self._min_idle_duration = min_idle_duration
        self._max_idle_duration = max_idle_duration
        self._min_attention_span = min_attention_span
        self._max_attention_span = max_attention_span
        self._issued_at = issued_at or get_current_datetime()

    def to_dict(self):

        def format_date(dt, fmt="%d/%m/%Y %H:%M"):
            if isinstance(dt, datetime):
                return dt.strftime(fmt)
            elif isinstance(dt, str):
                return dt  # já está no formato esperado
            return None

        data = {
            "lecture_id": self._lecture_id,
            "subject_id": self._subject_id,
            "lecture_alias": self._lecture_alias,
            "subject_name": self._subject_name,
            "teacher": self._teacher,
            "date_lecture": format_date(self._date_lecture, "%d/%m/%Y"),
            "total_students": self._total_students,

            "real_total_session_duration": self._real_total_session_duration,
            "avg_session_per_student": self._avg_session_per_student,
            "attendance_ratio": self._attendance_ratio,

            "lecture_focus_ratio": self._lecture_focus_ratio,
            "avg_focus_duration": self._avg_focus_duration,
            "max_focus_duration": self._max_focus_duration,

            "distraction_ratio": self._distraction_ratio,
            "distraction_frequency": self._distraction_frequency,
            "main_distractions": self._main_distractions,

            "total_time_watched": self._total_time_watched,
            "avg_lecture_duration": self._avg_lecture_duration,
            "avg_idle_duration": self._avg_idle_duration,
            "avg_attention_span": self._avg_attention_span,
            "pct_enabled_camera": self._pct_enabled_camera,
            "pct_enabled_mic": self._pct_enabled_mic,
            "avg_cam_streaming_span": self._avg_cam_streaming_span,
            "avg_mic_streaming_span": self._avg_mic_streaming_span,
            "min_lecture_duration": self._min_lecture_duration,
            "max_lecture_duration": self._max_lecture_duration,
            "min_idle_duration": self._min_idle_duration,
            "max_idle_duration": self._max_idle_duration,
            "min_attention_span": self._min_attention_span,
            "max_attention_span": self._max_attention_span,
            "issued_at": format_date(self._issued_at),
        }

        if self._id:
            data["_id"] = str(self._id)

        return data

    @staticmethod
    def from_dict(data):
        return Report(
            lecture_id=data["lecture_id"],
            subject_id=data["subject_id"],
            lecture_alias=data["lecture_alias"],
            subject_name=data.get("subject_name"),
            teacher=data.get("teacher"),
            date_lecture=data.get("date_lecture"),
            total_students=data.get("total_students", 0),
            distraction_ratio=data.get("distraction_ratio"),
            distraction_frequency=data.get("distraction_frequency"),
            main_distractions=data.get("main_distractions"),
            total_time_watched=data.get("total_time_watched", 0.0),
            avg_lecture_duration=data.get("avg_lecture_duration"),
            avg_idle_duration=data.get("avg_idle_duration"),
            avg_attention_span=data.get("avg_attention_span"),
            pct_enabled_camera=data.get("pct_enabled_camera"),
            pct_enabled_mic=data.get("pct_enabled_mic"),
            avg_cam_streaming_span=data.get("avg_cam_streaming_span"),
            avg_mic_streaming_span=data.get("avg_mic_streaming_span"),
            min_lecture_duration=data.get("min_lecture_duration"),
            max_lecture_duration=data.get("max_lecture_duration"),
            min_idle_duration=data.get("min_idle_duration"),
            max_idle_duration=data.get("max_idle_duration"),
            min_attention_span=data.get("min_attention_span"),
            max_attention_span=data.get("max_attention_span"),
            issued_at=data.get("issued_at"),
        )
