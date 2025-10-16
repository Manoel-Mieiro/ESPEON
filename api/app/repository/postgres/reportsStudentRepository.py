import uuid
from pg import conn
from app.models.postgres.reports_student import ReportStudent

cursor = conn.cursor()


def createReportStudent(report_student: ReportStudent):
    """
    Cria um novo relatório individual de aluno
    """
    try:
        report_student_id = str(uuid.uuid4())
        query = """
            INSERT INTO report_student (
                report_student_id,
                report_id,
                user_id,
                total_time_watched,
                attention_span,
                cam_enabled,
                mic_enabled,
                cam_streaming_span,
                mic_streaming_span
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING report_student_id
        """
        cursor.execute(query, (
            report_student_id,
            report_student._report_id,
            report_student._user_id,
            report_student._total_time_watched,
            report_student._attention_span,
            report_student._cam_enabled,
            report_student._mic_enabled,
            report_student._cam_streaming_span,
            report_student._mic_streaming_span
        ))
        conn.commit()
        report_student._id = report_student_id
        return report_student.to_dict()
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao criar report_student:", e)
        raise e


def findAllReportStudents():
    """
    Retorna todos os relatórios individuais
    """
    try:
        query = """
            SELECT
                report_student_id,
                report_id,
                user_id,
                total_time_watched,
                attention_span,
                cam_enabled,
                mic_enabled,
                cam_streaming_span,
                mic_streaming_span
            FROM report_student
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        reports = []

        for row in rows:
            rs = ReportStudent(
                report_id=row[1],
                user_id=row[2],
                total_time_watched=row[3],
                attention_span=row[4],
                cam_enabled=row[5],
                mic_enabled=row[6],
                cam_streaming_span=row[7],
                mic_streaming_span=row[8],
                _id=row[0]
            )
            reports.append(rs.to_dict())

        return reports
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar report_students:", e)
        raise e


def findReportStudentsByReport(report_id):
    """
    Retorna todos os alunos de um relatório específico
    """
    try:
        query = """
            SELECT
                report_student_id,
                report_id,
                user_id,
                total_time_watched,
                attention_span,
                cam_enabled,
                mic_enabled,
                cam_streaming_span,
                mic_streaming_span
            FROM report_student
            WHERE report_id = %s
        """
        cursor.execute(query, (report_id,))
        rows = cursor.fetchall()
        reports = []

        for row in rows:
            rs = ReportStudent(
                report_id=row[1],
                user_id=row[2],
                total_time_watched=row[3],
                attention_span=row[4],
                cam_enabled=row[5],
                mic_enabled=row[6],
                cam_streaming_span=row[7],
                mic_streaming_span=row[8],
                _id=row[0]
            )
            reports.append(rs.to_dict())

        return reports
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar report_students por report_id:", e)
        raise e


def deleteReportStudent(report_student_id):
    """
    Remove um relatório individual pelo ID
    """
    try:
        query = "DELETE FROM report_student WHERE report_student_id = %s"
        cursor.execute(query, (report_student_id,))
        conn.commit()
        return {"message": "Relatório de aluno removido com sucesso"}
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao remover report_student:", e)
        raise e
