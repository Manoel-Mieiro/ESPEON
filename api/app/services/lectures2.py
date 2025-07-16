import app.repository.lecturesRepository2 as lectures


def findAllLectures():
    try:
        lectureList = lectures.findAllLectures()
        for i, l in enumerate(lectureList):
            lectureList[i] = lectureStandardize(l)
        return lectureList
    except Exception as e:
        print("[SERVICE]Error fetching lectures:", e)
        raise e


def lectureStandardize(lecture):
    noUnderscore = lecture.replace("_", " ")
    return noUnderscore.upper()
