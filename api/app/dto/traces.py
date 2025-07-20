from app.models.traces import Traces
from app.models.roles import Roles


class TracesDTO:
    def __init__(
        self,
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
    ):
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

    def to_standard(self):
        return Traces(
            onlineClass=self.onlineClass,
            classTitle=self.classTitle,
            user=self.user,
            url=self.url,
            title=self.title,
            muted=self.muted,
            cameraEnabled=self.cameraEnabled,
            microphoneEnabled=self.microphoneEnabled,
            cameraStreaming=self.cameraStreaming,
            microphoneStreaming=self.microphoneStreaming,
            lastAccessed=self.lastAccessed,
            timestamp=self.timestamp,
            event=self.event,
        )
