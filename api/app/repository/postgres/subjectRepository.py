import uuid
from pg import conn
from app.models.postgres.subject import Subject

cursor = conn.cursor()


def createSubject(name: str) -> Subject:
    """
    Cria uma nova disciplina e retorna o objeto Subject criado
    """
    try:
        subject_id = str(uuid.uuid4())
        query = "INSERT INTO subject (subject_id, name) VALUES (%s, %s)"
        cursor.execute(query, (subject_id, name))
        conn.commit()
        return Subject(subject_id=subject_id, name=name)
    except Exception as e:
        print("[REPO][CREATE] Erro:", e)
        conn.rollback()
        return None


def findAllSubjects() -> list[Subject]:
    """
    Retorna todas as disciplinas como lista de objetos Subject
    """
    try:
        query = "SELECT subject_id, name FROM subject ORDER BY name"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Subject.from_row(row) for row in rows]
    except Exception as e:
        print("[REPO][FIND ALL] Erro:", e)
        return []


def findOneSubject(subject_id: str) -> Subject | None:
    """
    Retorna uma disciplina pelo ID como objeto Subject
    """
    try:
        query = "SELECT subject_id, name FROM subject WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        row = cursor.fetchone()
        return Subject.from_row(row) if row else None
    except Exception as e:
        print("[REPO][FIND BY ID] Erro:", e)
        return None


def updateSubject(subject_id: str, new_name: str) -> bool:
    """
    Atualiza o nome de uma disciplina, retorna True se houve atualização
    """
    try:
        query = "UPDATE subject SET name = %s WHERE subject_id = %s"
        cursor.execute(query, (new_name, subject_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("[REPO][UPDATE] Erro:", e)
        conn.rollback()
        return False


def deleteSubject(subject_id: str) -> bool:
    """
    Deleta uma disciplina, retorna True se houve exclusão
    """
    try:
        query = "DELETE FROM subject WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("[REPO][DELETE] Erro:", e)
        conn.rollback()
        return False
