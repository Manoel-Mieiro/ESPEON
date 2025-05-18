from bson import ObjectId


class Traces:
    def __init__(
        self,
        onlineClass: str,
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
        _id: ObjectId = None
    ):
        self._id = _id
        self.onlineClass = onlineClass
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

    def to_dict(self):
        data = {
            "onlineClass": self.onlineClass,
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
        }
        if self._id:
            data["_id"] = str(self._id)
        return data

    @staticmethod
    def from_dict(data):
        return Traces(
            onlineClass=data["onlineClass"],
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
            _id=data.get("_id")
        )
