import app.services.reports.raw as raw
import datetime


def builReport(subject=None, lecture=None):
    try:
        if subject:
            data = raw.findAllTraces(subject)
        elif lecture:
            data = raw.findLecture(lecture)
        return assembleData(data, subject, lecture)
    except Exception as e:
        raise e


def countDistinct(arr):
    distinct = set(arr)
    return len(distinct)


def assembleData(logs, subject=None, lectureId=None):
    subject = get_subject(logs, subject, lectureId)
    countLecutre = count_lecture(logs) if not lectureId else None
    countStudents = count_students(logs)
    totalTimeWatched = total_time_watched(logs)
    avgLectureDuration = avg_lecture_duration(logs) if not lectureId else None
    avgIdleDuration = avg_idle_duration(logs)
    avgAttentionSpan = avg_attention_span(logs)
    pctEnabledCamera = boolPercentage(logs, "cameraEnabled")
    pctEnabledMic = boolPercentage(logs, "microphoneEnabled")
    avgCamStreamingSpan = boolPercentage(logs, "cameraStreaming")
    avgMicStreamingSpan = boolPercentage(logs, "microphoneStreaming")
    lecture = get_lecture(lectureId) if lectureId else None
    issuedAt = issueDate()
    return {
        "subject": subject,
        "lecture": lecture,
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
        "issuedAt": issuedAt,
    }


def get_subject(logs, subject=None, lectureId=None):
    if lectureId:
        data = raw.extractField(logs, "subject")
        return data
    else:
        return subject


def get_lecture(lectureId):
    data = raw.findLecture(lectureId)
    lecture = raw.extractField(data, "_id")
    return lecture


def count_lecture(logs):
    data = raw.extractField(logs, "classTitle")
    print(type(data))
    return countDistinct(data)


def count_students(logs):
    data = raw.extractField(logs, "user")
    return countDistinct(data)


def total_time_watched(logs):
    total = calculate_class_duration(logs)
    print(f"[total_time_watched] total is ", total)
    return total


def calculate_class_duration(period):
    start_hour, start_minute = map(int, period["period_start"].split(":"))
    end_hour, end_minute = map(int, period["period_end"].split(":"))

    print(f"start_hour = {start_hour} | end_hour = {end_hour}")
    total_minutes = (end_hour * 60 + end_minute) - \
        (start_hour * 60 + start_minute)
    return round((total_minutes / 60), 2)


def avg_lecture_duration(logs):
    return 1  # por enquanto vou retornar 1


def avg_idle_duration(logs):
    return 1  # por enquanto vou retornar 1


def avg_attention_span(logs):
    return 0  # por enquanto vou retornar 0


def issueDate():
    now = datetime.datetime.now()
    date = now.strftime("%c")
    print(f"Current date is: {date}")
    return date


def boolPercentage(logs, field):
    data = raw.extractField(logs, field)
    occurences = data.count("yes")
    total = 1
    if len(data) > 0:
        total = len(data)
    return occurences/total
