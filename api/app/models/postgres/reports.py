from bson import ObjectId
from datetime import datetime, date
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

        lecture_length: float = None,
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

        engagement_score: float = None,
        attention_health: float = None,
        distraction_risk: float = None,

        issued_at: datetime = None,
        _id: ObjectId = None
    ):
        self._id = _id
        self._lecture_id = lecture_id
        self._subject_id = subject_id
        self._lecture_alias = lecture_alias
        self._subject_name = subject_name
        self._teacher = teacher
        self._date_lecture = parse_date(date_lecture)
        self._total_students = total_students

        self._lecture_length = lecture_length
        self._avg_session_per_student = avg_session_per_student
        self._attendance_ratio = attendance_ratio

        self._lecture_focus_ratio = lecture_focus_ratio
        self._avg_focus_duration = avg_focus_duration
        self._max_focus_duration = max_focus_duration

        self._distraction_ratio = distraction_ratio
        self._distraction_frequency = distraction_frequency
        self._main_distractions = main_distractions

        self._tab_switch_frequency = tab_switch_frequency
        self._multitasking_intensity = multitasking_intensity
        self._focus_fragmentation = focus_fragmentation

        self._camera_engagement = camera_engagement
        self._mic_engagement = mic_engagement
        self._voluntary_participation = voluntary_participation

        self._engagement_trend = engagement_trend or {
            "q1": 0.0,
            "q2": 0.0,
            "q3": 0.0,
            "q4": 0.0
        }

        self._peak_engagement_time = peak_engagement_time
        self._dropoff_point = dropoff_point

        self._engagement_score = engagement_score
        self._attention_health = attention_health
        self._distraction_risk = distraction_risk

        self._issued_at = issued_at or get_current_datetime()

    def to_dict(self):

        def format_date(dt, fmt="%d/%m/%Y %H:%M"):
            if isinstance(dt, datetime):
                return dt.strftime(fmt)
            elif isinstance(dt, str):
                return dt
            return None

        data = {
            "lecture_id": self._lecture_id,
            "subject_id": self._subject_id,
            "lecture_alias": self._lecture_alias,
            "subject_name": self._subject_name,
            "teacher": self._teacher,
            "date_lecture": format_date(self._date_lecture, "%d/%m/%Y"),
            "total_students": self._total_students,

            "lecture_length": self._lecture_length,
            "avg_session_per_student": self._avg_session_per_student,
            "attendance_ratio": self._attendance_ratio,

            "lecture_focus_ratio": self._lecture_focus_ratio,
            "avg_focus_duration": self._avg_focus_duration,
            "max_focus_duration": self._max_focus_duration,

            "distraction_ratio": self._distraction_ratio,
            "distraction_frequency": self._distraction_frequency,
            "main_distractions": self._main_distractions,

            "tab_switch_frequency": self._tab_switch_frequency,
            "multitasking_intensity": self._multitasking_intensity,
            "focus_fragmentation": self._focus_fragmentation,

            "camera_engagement": self._camera_engagement,
            "mic_engagement": self._mic_engagement,
            "voluntary_participation": self._voluntary_participation,

            "engagement_trend": self._engagement_trend,
            "peak_engagement_time": self._peak_engagement_time,
            "dropoff_point": self._dropoff_point,

            "engagement_score": self._engagement_score,
            "attention_health": self._attention_health,
            "distraction_risk": self._distraction_risk,

            "issued_at": format_date(self._issued_at),
        }

        if self._id:
            data["_id"] = str(self._id)

        return data

    @staticmethod
    def from_dict(data):
        _id = data.get('report_id') or data.get('_id')
        return Report(
             _id=_id,
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

            tab_switch_frequency=data.get("tab_switch_frequency"),
            multitasking_intensity=data.get("multitasking_intensity"),
            focus_fragmentation=data.get("focus_fragmentation"),

            camera_engagement=data.get("camera_engagement"),
            mic_engagement=data.get("mic_engagement"),
            voluntary_participation=data.get("voluntary_participation"),

            engagement_trend=data.get("engagement_trend"),
            peak_engagement_time=data.get("peak_engagement_time"),
            dropoff_point=data.get("dropoff_point"),
            engagement_score=data.get("engagement_score"),
            attention_health=data.get("attention_health"),
            distraction_risk=data.get("distraction_risk"),

            issued_at=data.get("issued_at"),
        )

def parse_date(value):
    if value is None:
        return datetime.utcnow()

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except:
            pass

    return datetime.utcnow()