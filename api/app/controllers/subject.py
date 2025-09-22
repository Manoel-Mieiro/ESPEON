import app.services.postgres.subject as subjectService


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
        name = data.get("name")
        if not name:
            raise ValueError("Campo 'name' é obrigatório")
        return subjectService.createSubject(name)
    except Exception as e:
        print("[CONTROLLER] Error creating subject:", e)
        raise e


def updateSubject(subject_id, updatedData):
    try:
        new_name = updatedData.get("name")
        if not new_name:
            raise ValueError("Campo 'name' é obrigatório para atualização")
        return subjectService.updateSubject(subject_id, new_name)
    except Exception as e:
        print("[CONTROLLER] Error updating subject:", e)
        raise e


def deleteSubject(subject_id):
    try:
        return subjectService.deleteSubject(subject_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting subject:", e)
        raise e
