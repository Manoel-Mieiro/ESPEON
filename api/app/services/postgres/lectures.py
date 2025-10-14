import app.repository.postgres.lecturesRepository as lectures


def findAllLectures():
    try:
        return lectures.findAllLectures()
    except Exception as e:
        print("[SERVICE] Error fetching lectures:", e)
        raise e


def createLecture(lecture):
    """
    Recebe um objeto Lecture e envia para o repository
    """
    try:
        return lectures.createLecture(lecture)
    except Exception as e:
        print("[SERVICE] Error creating lecture:", e)
        raise e


def findOneLecture(lecture_id: str):
    try:
        return lectures.findOneLecture(lecture_id)
    except Exception as e:
        print("[SERVICE] Error fetching lecture:", e)
        raise e


def updateLecture(lecture_id: str, lecture_data):
    """
    Recebe um dicionário ou um objeto Lecture, envia para o repository
    """
    try:
        if hasattr(lecture_data, "to_dict"):
            lecture_data = lecture_data.to_dict()
        return lectures.updateLecture(lecture_id, lecture_data)
    except Exception as e:
        print("[SERVICE] Error updating lecture:", e)
        raise e


def deleteLecture(lecture_id: str):
    try:
        return lectures.deleteLecture(lecture_id)
    except Exception as e:
        print("[SERVICE] Error deleting lecture:", e)
        raise e


def findLecturesBySubject(subject_id: str):
    try:
        return lectures.findLecturesBySubject(subject_id)
    except Exception as e:
        print("[SERVICE] Error fetching lectures:", e)
        raise e
