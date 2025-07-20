import app.services.reports.raw as raw


def builReport(subject):
    try:
        data = raw.findAllTraces(subject)
        return assembleData()
    except Exception as e:
        raise e


def assembleData():
    countLecutre = ""
    countStudents = ""
    totalTimeWatched = ""
    avgLectureDuration = ""
    avgIdleDuration = ""
    avgAttentionSpan = ""
    pctEnabledCamera = ""
    pctEnabledMic = ""
    avgCamStreamingSpan = ""
    avgMicStreamingSpan = ""
    return {
        "countLecutre": "self.countLecutre",
        "countStudents": "self.countLecutre",
        "totalTimeWatched": "self.countLecutre",
        "avgLectureDuration": "self.countLecutre",
        "avgIdleDuration": "self.countLecutre",
        "avgAttentionSpan": "self.countLecutre",
        "pctEnabledCamera": "self.countLecutre",
        "pctEnabledMic": "self.countLecutre",
        "avgCamStreamingSpan": "self.countLecutre",
        "avgMicStreamingSpan": "self.countLecutre",
    }

def countLecture():
    data = raw.extractField("countLecutre")