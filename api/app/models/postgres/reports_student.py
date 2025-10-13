from bson import ObjectId


class ReportStudent:
    def __init__(
        self,
        report_id: str,
        user_id: str,
        total_time_watched: float = None,
        attention_span: float = None,
        cam_enabled: bool = None,
        mic_enabled: bool = None,
        cam_streaming_span: float = None,
        mic_streaming_span: float = None,
        _id: ObjectId = None
    ):
        self._id = _id
        self._report_id = report_id
        self._user_id = user_id
        self._total_time_watched = total_time_watched
        self._attention_span = attention_span
        self._cam_enabled = cam_enabled
        self._mic_enabled = mic_enabled
        self._cam_streaming_span = cam_streaming_span
        self._mic_streaming_span = mic_streaming_span

    def to_dict(self):
        data = {
            "report_id": self._report_id,
            "user_id": self._user_id,
            "total_time_watched": self._total_time_watched,
            "attention_span": self._attention_span,
            "cam_enabled": self._cam_enabled,
            "mic_enabled": self._mic_enabled,
            "cam_streaming_span": self._cam_streaming_span,
            "mic_streaming_span": self._mic_streaming_span
        }
        if self._id:
            data["_id"] = str(self._id)
        return data

    @staticmethod
    def from_dict(data):
        return ReportStudent(
            report_id=data["report_id"],
            user_id=data["user_id"],
            total_time_watched=data.get("total_time_watched"),
            attention_span=data.get("attention_span"),
            cam_enabled=data.get("cam_enabled"),
            mic_enabled=data.get("mic_enabled"),
            cam_streaming_span=data.get("cam_streaming_span"),
            mic_streaming_span=data.get("mic_streaming_span"),
        )
