import app.services.reports.raw as raw


def builReport(subject):
    try:
        data = raw.findAllTraces(subject)
        return assembleData(data)
    except Exception as e:
        raise e


def countDistinct(arr):
    distinct = set(arr)
    return len(distinct)


def assembleData(logs):
    countLecutre = count_lecture(logs)
    countStudents = count_students(logs)
    totalTimeWatched = total_time_watched(logs)
    avgLectureDuration = avg_lecture_duration(logs)
    avgIdleDuration = avg_idle_duration(logs)
    avgAttentionSpan = avg_attention_span(logs)
    pctEnabledCamera = boolPercentage(logs, "cameraEnabled")
    pctEnabledMic = boolPercentage(logs, "microphoneEnabled")
    avgCamStreamingSpan = boolPercentage(logs, "cameraStreaming")
    avgMicStreamingSpan = boolPercentage(logs, "microphoneStreaming")
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


def count_lecture(logs):
    data = raw.extractField(logs, "classTitle")
    return countDistinct(data)


def count_students(logs):
    data = raw.extractField(logs, "user")
    return countDistinct(data)


def total_time_watched(logs):
    return 0  # por enquanto vou retornar 0


def avg_lecture_duration(logs):
    return 1  # por enquanto vou retornar 1


def avg_idle_duration(logs):
    return 1  # por enquanto vou retornar 1


def avg_attention_span(logs):
    return 0  # por enquanto vou retornar 0


def boolPercentage(logs, field):
    data = raw.extractField(logs, field)
    occurences = data.count("yes")
    total = 1
    if len(data) > 0:
        total = len(data)
    return occurences/total
