# import app.services.lectures as lectureService
# from app.dto.lectures import LectureDTO


# def findAllLectures():
#     try:
#         return lectureService.findAllLectures()
#     except Exception as e:
#         print("[CONTROLLER]Error fetching lectures:", e)
#         raise e


# def createLecture(data):
#     try:
#         lec = LectureDTO(
#             subject=data["subject"],
#             date_lecture=data["date_lecture"],
#             period_start=data["period_start"],
#             period_end=data["period_end"],
#             teacher=data["teacher"],
#         )
#         return lectureService.createLecture(lec.to_standard())
#     except Exception as e:
#         print("[CONTROLLER]Error creating lecture:", e)
#         raise e


# def findOneLecture(_id):
#     try:
#         fetched = lectureService.findOneLecture(_id)
#         if not fetched:
#             raise Exception(f"Lecture {_id} não encontrado")
#         return fetched
#     except Exception as e:
#         print("[CONTROLLER]Error fetching lecture:", e)
#         raise e


# def updateLecture(_id, updatedLecture):
#     try:
#         return lectureService.updateLecture(_id, updatedLecture)
#     except Exception as e:
#         print("[CONTROLLER]Error updating lecture:", e)
#         raise e


# def deleteLecture(_id):
#     try:
#         return lectureService.deleteLecture(_id)
#     except Exception as e:
#         print("[CONTROLLER]Error deleting lecture:", e)
#         raise e
