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
        lectureId: str = None,
        lectureMuted: bool = False,
        lectureTabState: str = None,
        lectureTabLastAccessed: str = None,
        lectureAudible: bool = None,
        lectureMutedInfoReason: str = None,
    ):
        self.lectureId = lectureId
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

    def to_standard(self):
        return Traces(
            lecture_id=self.lectureId,
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
            lectureMuted=self.lectureMuted,
            lectureTabState=self.lectureTabState,
            lectureTabLastAccessed=self.lectureTabLastAccessed,
            lectureAudible=self.lectureAudible,
            lectureMutedInfoReason=self.lectureMutedInfoReason,
        )
