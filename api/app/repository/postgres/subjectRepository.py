import uuid
from pg import conn

cursor = conn.cursor()


def createSubject(name: str):
    try:
        query = "INSERT INTO subject (subject_id, name) VALUES (%s, %s) RETURNING subject_id"
        subject_id = str(uuid.uuid4())
        cursor.execute(query, (subject_id, name))
        conn.commit()
        return subject_id
    except Exception as e:
        print("[REPO][CREATE] Erro:", e)
        conn.rollback()
        return None


def findAllSubjects():
    try:
        query = "SELECT subject_id, name FROM subject ORDER BY name"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("[REPO][FIND ALL] Erro:", e)
        return []


def findOneSubject(subject_id: str):
    try:
        query = "SELECT subject_id, name FROM subject WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        return cursor.fetchone()
    except Exception as e:
        print("[REPO][FIND BY ID] Erro:", e)
        return None


def updateSubject(subject_id: str, new_name: str):
    try:
        query = "UPDATE subject SET name = %s WHERE subject_id = %s"
        cursor.execute(query, (new_name, subject_id))
        conn.commit()
        return cursor.rowcount  # número de linhas afetadas
    except Exception as e:
        print("[REPO][UPDATE] Erro:", e)
        conn.rollback()
        return 0


def deleteSubject(subject_id: str):
    try:
        query = "DELETE FROM subject WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        conn.commit()
        return cursor.rowcount  # número de linhas deletadas
    except Exception as e:
        print("[REPO][DELETE] Erro:", e)
        conn.rollback()
        return 0
