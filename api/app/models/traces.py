from bson import ObjectId

class Traces:
    def __init__(
        self,
        lecture_id: str,
        onlineClass: str,
        classTitle: str,
        user: str,
        url: str,
        title: str,
        muted: bool,
        cameraEnabled: bool,
        microphoneEnabled: bool,
        cameraStreaming: bool,
        microphoneStreaming: bool,
        lastAccessed: str,
        timestamp: str,
        event: str,
        lectureMuted: bool = False,
        lectureTabState: str = None,
        lectureTabLastAccessed: str = None,
        lectureAudible: bool = None,
        lectureMutedInfoReason: str = None,
        _id: ObjectId = None
    ):
        self._id = _id
        self.lecture_id = lecture_id
        self.onlineClass = onlineClass
        self.classTitle = classTitle
        self.user = user
        self.url = url
        self.title = title
        self.muted = muted
        self.cameraEnabled = cameraEnabled
        self.microphoneEnabled = microphoneEnabled
        self.cameraStreaming = cameraStreaming
        self.microphoneStreaming = microphoneStreaming
        self.lastAccessed = lastAccessed
        self.timestamp = timestamp
        self.event = event
        self.lectureMuted = lectureMuted
        self.lectureTabState = lectureTabState
        self.lectureTabLastAccessed = lectureTabLastAccessed
        self.lectureAudible = lectureAudible
        self.lectureMutedInfoReason = lectureMutedInfoReason

    def to_dict(self):
        data = {
            "lectureId": self.lecture_id,
            "onlineClass": self.onlineClass,
            "classTitle":  self.classTitle,
            "user": self.user,
            "url": self.url,
            "title": self.title,
            "muted": self.muted,
            "cameraEnabled": self.cameraEnabled,
            "microphoneEnabled": self.microphoneEnabled,
            "cameraStreaming": self.cameraStreaming,
            "microphoneStreaming": self.microphoneStreaming,
            "lastAccessed": self.lastAccessed,
            "timestamp": self.timestamp,
            "event": self.event,
            "lectureMuted": self.lectureMuted,
            "lectureTabState": self.lectureTabState,
            "lectureTabLastAccessed": self.lectureTabLastAccessed,
            "lectureAudible": self.lectureAudible,
            "lectureMutedInfoReason": self.lectureMutedInfoReason,
        }
        if self._id:
            data["_id"] = str(self._id)
        return data

    @staticmethod
    def from_dict(data):
        return Traces(
            lecture_id=data["lectureId"],
            onlineClass=data["onlineClass"],
            classTitle=data["classTitle"],
            user=data["user"],
            url=data["url"],
            title=data["title"],
            muted=data["muted"],
            cameraEnabled=data["cameraEnabled"],
            microphoneEnabled=data["microphoneEnabled"],
            cameraStreaming=data["cameraStreaming"],
            microphoneStreaming=data["microphoneStreaming"],
            lastAccessed=data["lastAccessed"],
            timestamp=data["timestamp"],
            event=data["event"],
            lectureMuted=data.get("lectureMuted", False),
            lectureTabState=data.get("lectureTabState"),
            lectureTabLastAccessed=data.get("lectureTabLastAccessed"),
            lectureAudible=data.get("lectureAudible"),
            lectureMutedInfoReason=data.get("lectureMutedInfoReason"),
            _id=data.get("_id")
        )
