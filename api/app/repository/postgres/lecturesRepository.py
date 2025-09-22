import uuid
from pg import conn
from app.models.postgres.lecture import Lecture

cursor = conn.cursor()


def createLecture(lecture):
    """
    lecture: objeto Lecture (com propriedades: subject_id, teacher_id, date_lecture, period_start, period_end)
    """
    try:
        lecture_id = str(uuid.uuid4())
        query = """
            INSERT INTO lecture (
                lecture_id, subject_id, teacher_id, date_lecture, period_start, period_end
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING lecture_id
        """
        cursor.execute(query, (
            lecture_id,
            lecture.subject_id,
            lecture.teacher_id,
            lecture.date_lecture,
            lecture.period_start,
            lecture.period_end
        ))
        conn.commit()
        lecture.lecture_id = lecture_id
        return lecture.to_dict()
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY]Erro ao criar lecture:", e)
        raise e


def findAllLectures():
    try:
        query = """
            SELECT lecture_id, subject_id, teacher_id, date_lecture, period_start, period_end
            FROM lecture
            ORDER BY date_lecture DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        lectures_list = []

        for row in rows:
            lecture = Lecture(
                lecture_id=row[0],
                subject_id=row[1],
                teacher_id=row[2],
                date_lecture=row[3],
                period_start=row[4],
                period_end=row[5]
            )
            lectures_list.append(lecture.to_dict())

        return lectures_list
    except Exception as e:
        print("[REPOSITORY]Erro ao buscar aulas:", e)
        raise e


def findOneLecture(lecture_id):
    try:
        query = """
            SELECT lecture_id, subject_id, teacher_id, date_lecture, period_start, period_end
            FROM lecture
            WHERE lecture_id = %s
        """
        cursor.execute(query, (lecture_id,))
        row = cursor.fetchone()
        if not row:
            return None

        lecture = Lecture(
            lecture_id=row[0],
            subject_id=row[1],
            teacher_id=row[2],
            date_lecture=row[3],
            period_start=row[4],
            period_end=row[5]
        )
        return lecture.to_dict()
    except Exception as e:
        print("[REPOSITORY]Erro ao buscar aula:", e)
        raise e


def updateLecture(lecture_id, updatedLecture: dict):
    try:
        query = """
            UPDATE lecture
            SET subject_id = %s,
                teacher_id = %s,
                date_lecture = %s,
                period_start = %s,
                period_end = %s
            WHERE lecture_id = %s
        """
        cursor.execute(query, (
            updatedLecture["subject_id"],
            updatedLecture["teacher_id"],
            updatedLecture["date_lecture"],
            updatedLecture["period_start"],
            updatedLecture["period_end"],
            lecture_id
        ))
        conn.commit()
        return findOneLecture(lecture_id)
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY]Erro ao atualizar lecture:", e)
        raise e


def deleteLecture(lecture_id):
    try:
        query = "DELETE FROM lecture WHERE lecture_id = %s"
        cursor.execute(query, (lecture_id,))
        conn.commit()
        return {"message": "Aula removida com sucesso"}
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY]Erro ao remover aula:", e)
        raise e
