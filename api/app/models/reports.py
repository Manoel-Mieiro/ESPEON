from bson import ObjectId


class Reports:
    def __init__(
        self,
        subject: str,
        countStudents: int,
        totalTimeWatched: float,
        avgLectureDuration: float,
        avgIdleDuration: float,
        avgAttentionSpan: float,
        pctEnabledCamera: float,
        pctEnabledMic: float,
        avgCamStreamingSpan: float,
        avgMicStreamingSpan: float,
        issuedAt: float,
        _id: ObjectId = None,
        countLecutre: int = None,
        lecture: str = None
    ):
        self._id = _id
        self.lecture = lecture
        self.subject = subject
        self.countLecutre = countLecutre
        self.countStudents = countStudents
        self.totalTimeWatched = totalTimeWatched
        self.avgLectureDuration = avgLectureDuration
        self.avgIdleDuration = avgIdleDuration
        self.avgAttentionSpan = avgAttentionSpan
        self.pctEnabledCamera = pctEnabledCamera
        self.pctEnabledMic = pctEnabledMic
        self.avgCamStreamingSpan = avgCamStreamingSpan
        self.avgMicStreamingSpan = avgMicStreamingSpan
        self.issuedAt = issuedAt

    def to_dict(self):
        data = {
            "subject": self.subject,
            "countStudents": self.countStudents,
            "totalTimeWatched": self.totalTimeWatched,
            "avgLectureDuration": self.avgLectureDuration,
            "avgIdleDuration": self.avgIdleDuration,
            "avgAttentionSpan": self.avgAttentionSpan,
            "pctEnabledCamera": self.pctEnabledCamera,
            "pctEnabledMic": self.pctEnabledMic,
            "avgCamStreamingSpan": self.avgCamStreamingSpan,
            "avgMicStreamingSpan": self.avgMicStreamingSpan,
            "issuedAt": self.issuedAt,
        }
        if self._id:
            data["_id"] = str(self._id)
        if self.lecture:
            data["lecture"] = self.lecture
        if self.countLecutre:
            data["countLecutre"] = self.countLecutre
        return data

    @staticmethod
    def from_dict(data):
        return Reports(
            subject=data["subject"],
            countStudents=data["countStudents"],
            totalTimeWatched=data["totalTimeWatched"],
            avgLectureDuration=data["avgLectureDuration"],
            avgIdleDuration=data["avgIdleDuration"],
            avgAttentionSpan=data["avgAttentionSpan"],
            pctEnabledCamera=data["pctEnabledCamera"],
            pctEnabledMic=data["pctEnabledMic"],
            avgCamStreamingSpan=data["avgCamStreamingSpan"],
            avgMicStreamingSpan=data["avgMicStreamingSpan"],
            issuedAt=data["issuedAt"],
            _id=data.get("_id"),
            lecture=data.get("lecture"),
            countLecutre=data.get("countLecture"),
        )
