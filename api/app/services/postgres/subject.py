import app.repository.postgres.subjectRepository as subjects
from app.models.postgres.subject import Subject


def findAllSubjects():
    try:
        all_subjects = subjects.findAllSubjects()
        return [s.to_dict() for s in all_subjects]
    except Exception as e:
        print("[SERVICE] Error fetching subjects:", e)
        raise e


def findOneSubject(subject_id=None):
    try:
        if not subject_id:
            raise Exception("subject_id é obrigatório!")
        subject = subjects.findOneSubject(subject_id)
        return subject.to_dict() if subject else None
    except Exception as e:
        print("[SERVICE] Error fetching subject:", e)
        raise e


def createSubject(name):
    try:
        all_subjects = subjects.findAllSubjects()
        if any(s.name == name for s in all_subjects):
            raise Exception("Matéria já existe!")
        new_subject = subjects.createSubject(name)
        return new_subject.to_dict()
    except Exception as e:
        print("[SERVICE] Error creating subject:", e)
        raise e


def updateSubject(subject_id, new_name):
    try:
        all_subjects = subjects.findAllSubjects()
        if any(s.name == new_name and s.subject_id != subject_id for s in all_subjects):
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
