from bson import ObjectId


class Reports:
    def __init__(
        self,
        countLecutre: int,
        countStudents: int,
        totalTimeWatched: float,
        avgLectureDuration: float,
        avgIdleDuration: float,
        avgAttentionSpan: float,
        pctEnabledCamera: float,
        pctEnabledMic: float,
        avgCamStreamingSpan: float,
        avgMicStreamingSpan: float,
        _id: ObjectId = None
    ):
        self._id = _id
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

    def to_dict(self):
        data = {
            "countLecutre": self.countLecutre,
            "countStudents": self.countStudents,
            "totalTimeWatched": self.totalTimeWatched,
            "avgLectureDuration": self.avgLectureDuration,
            "avgIdleDuration": self.avgIdleDuration,
            "avgAttentionSpan": self.avgAttentionSpan,
            "pctEnabledCamera": self.pctEnabledCamera,
            "pctEnabledMic": self.pctEnabledMic,
            "avgCamStreamingSpan": self.avgCamStreamingSpan,
            "avgMicStreamingSpan": self.avgMicStreamingSpan,
        }
        if self._id:
            data["_id"] = str(self._id)
        return data

    @staticmethod
    def from_dict(data):
        return Reports(
            countLecutre=data["countLecutre"],
            countStudents=data["countStudents"],
            totalTimeWatched=data["totalTimeWatched"],
            avgLectureDuration=data["avgLectureDuration"],
            avgIdleDuration=data["avgIdleDuration"],
            avgAttentionSpan=data["avgAttentionSpan"],
            pctEnabledCamera=data["pctEnabledCamera"],
            pctEnabledMic=data["pctEnabledMic"],
            avgCamStreamingSpan=data["avgCamStreamingSpan"],
            avgMicStreamingSpan=data["avgMicStreamingSpan"],
            _id=data.get("_id")
        )
