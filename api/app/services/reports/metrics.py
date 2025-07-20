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
    totalTimeWatched = totalTimeWatched()
    avgLectureDuration = avgLectureDuration()
    avgIdleDuration = avgIdleDuration()
    avgAttentionSpan = avgAttentionSpan()
    pctEnabledCamera = boolPercentage("cameraEnabled")
    pctEnabledMic = boolPercentage("microphoneEnabled")
    avgCamStreamingSpan = boolPercentage("cameraStreaming")
    avgMicStreamingSpan = boolPercentage("microphoneStreaming")
    return {
        "countLecutre": countLecutre,
        "countStudents": countStudents,
        "totalTimeWatched": totalTimeWatched,
        "avgLectureDuration": avgLectureDuration,
        "avgIdleDuration": avgIdleDuration,
        "avgAttentionSpan": avgAttentionSpan,
        "pctEnabledCamera": pctEnabledCamera,
        "pctEnabledMic": pctEnabledMic,
        "avgCamStreamingSpan": avgCamStreamingSpan,
        "avgMicStreamingSpan": avgMicStreamingSpan,
    }


def countLecture():
    data = raw.extractField("classTitle")
    return countDistinct(data)


def countStudents():
    data = raw.extractField("user")
    return countDistinct(data)


def totalTimeWatched():
    return 0  # por enquanto vou retornar 0


def avgLectureDuration():
    return 1  # por enquanto vou retornar 1


def avgIdleDuration():
    return 1  # por enquanto vou retornar 1


def avgAttentionSpan():
    return 0  # por enquanto vou retornar 0


def boolPercentage(field):
    data = raw.extractField(field)
    occurences = data.count("yes")
    return occurences/len(data)
