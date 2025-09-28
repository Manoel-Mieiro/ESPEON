from app.services.postgres.lectures import lectures as lectureService
from app.dto.postgres.lectures import LectureDTO

def findAllLectures():
    try:
        return lectureService.findAllLectures()
    except Exception as e:
        print("[CONTROLLER] Error fetching lectures:", e)
        raise e


def createLecture(data):
    try:
        lec_dto = LectureDTO(
            subject_id=data["subject_id"],
            teacher_id=data["teacher_id"],
            date_lecture=data["date_lecture"],
            period_start=data["period_start"],
            period_end=data["period_end"]
        )
        lecture = lec_dto.to_standard()
        return lectureService.createLecture(lecture)
    except Exception as e:
        print("[CONTROLLER] Error creating lecture:", e)
        raise e


def findOneLecture(lecture_id):
    try:
        fetched = lectureService.findOneLecture(lecture_id)
        if not fetched:
            raise Exception(f"Lecture {lecture_id} não encontrada")
        return fetched
    except Exception as e:
        print("[CONTROLLER] Error fetching lecture:", e)
        raise e


def updateLecture(lecture_id, data):
    try:
        lec_dto = LectureDTO(
            subject_id=data["subject_id"],
            teacher_id=data["teacher_id"],
            date_lecture=data["date_lecture"],
            period_start=data["period_start"],
            period_end=data["period_end"]
        )
        updated_lecture = lec_dto.to_standard()
        return lectureService.updateLecture(lecture_id, updated_lecture.to_dict())
    except Exception as e:
        print("[CONTROLLER] Error updating lecture:", e)
        raise e


def deleteLecture(lecture_id):
    try:
        return lectureService.deleteLecture(lecture_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting lecture:", e)
        raise e
