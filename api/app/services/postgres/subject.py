import app.repository.postgres.subjectRepository as subjects

def findAllSubjects():
    try:
        return subjects.findAllSubjects()
    except Exception as e:
        print("[SERVICE] Error fetching subjects:", e)
        raise e

def findOneSubject(subject_id=None):
    try:
        if not subject_id:
            raise Exception("subject_id é obrigatório!")
        return subjects.findOneSubject(subject_id)
    except Exception as e:
        print("[SERVICE] Error fetching subject:", e)
        raise e


def createSubject(name):
    try:
        all_subjects = findAllSubjects()
        if any(s[1] == name for s in all_subjects):
            raise Exception("Matéria já existe!")
        return subjects.createSubject(name)
    except Exception as e:
        print("[SERVICE] Error creating subject:", e)
        raise e


def updateSubject(subject_id, new_name):
    try:
        all_subjects = findAllSubjects()
        if any(s[1] == new_name for s in all_subjects if s[0] != subject_id):
            raise Exception("Já existe uma matéria com esse nome!")
        return subjects.updateSubject(subject_id, new_name)
    except Exception as e:
        print("[SERVICE] Error updating subject:", e)
        raise e

def deleteSubject(subject_id):
    try:
        return subjects.deleteSubject(subject_id)
    except Exception as e:
        print("[SERVICE] Error deleting subject:", e)
        raise e
