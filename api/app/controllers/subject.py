import app.services.postgres.subject as subjectService
from app.dto.postgres.subject import SubjectDTO

def findAllSubjects():
    try:
        return subjectService.findAllSubjects()
    except Exception as e:
        print("[CONTROLLER] Error fetching subjects:", e)
        raise e

def findOneSubject(subject_id):
    try:
        return subjectService.findOneSubject(subject_id)
    except Exception as e:
        print("[CONTROLLER] Error fetching subject:", e)
        raise e

def createSubject(data):
    try:
        subject = SubjectDTO(
            name=data["name"]
        )
        return subjectService.createSubject(subject.to_standard())
    except Exception as e:
        print("[CONTROLLER] Error creating subject:", e)
        raise e

def updateSubject(subject_id, updatedData):
    try:
        return subjectService.updateSubject(subject_id, updatedData["name"])
    except Exception as e:
        print("[CONTROLLER] Error updating subject:", e)
        raise e

def deleteSubject(subject_id):
    try:
        return subjectService.deleteSubject(subject_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting subject:", e)
        raise e
