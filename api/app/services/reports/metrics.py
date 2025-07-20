import app.services.reports.raw as raw


def builReport(subject):
    try:
        data = raw.findAllTraces(subject)
        return assembleData()
    except Exception as e:
        raise e

def countDistinct(arr):
    distinct = set(arr)
    return len(distinct)

def assembleData():
    countLecutre = countLecture()
    countStudents = countStudents()
    totalTimeWatched = ""
    avgLectureDuration = ""
    avgIdleDuration = ""
    avgAttentionSpan = ""
    pctEnabledCamera = ""
    pctEnabledMic = ""
    avgCamStreamingSpan = ""
    avgMicStreamingSpan = ""
    return {
        "countLecutre": countLecutre,
        "countStudents": countStudents,
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
    data = raw.extractField("classTitle")
    return countDistinct(data)

def countStudents():
    data = raw.extractField("user")
    return countDistinct(data)