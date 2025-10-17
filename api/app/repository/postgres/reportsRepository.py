import uuid
from pg import conn
from app.models.postgres.reports import Report

cursor = conn.cursor()



def createReport(report: Report):
    """
    Cria um novo relatório agregado (por aula/disciplina).
    """
    try:
        report_id = str(uuid.uuid4())
        query = """
            INSERT INTO report (
                report_id,
                lecture_id,
                subject_id,
                total_students,
                total_time_watched,
                avg_lecture_duration,
                avg_idle_duration,
                avg_attention_span,
                pct_enabled_camera,
                pct_enabled_mic,
                avg_cam_streaming_span,
                avg_mic_streaming_span,
                issued_at
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING *;
        """
        cursor.execute(query, (
            report_id,
            report._lecture_id,
            report._subject_id,
            report._total_students,
            report._total_time_watched,
            report._avg_lecture_duration,
            report._avg_idle_duration,
            report._avg_attention_span,
            report._pct_enabled_camera,
            report._pct_enabled_mic,
            report._avg_cam_streaming_span,
            report._avg_mic_streaming_span,
            report._issued_at
        ))
        conn.commit()
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao criar report:", e)
        raise e


def findAllReports():
    """
    Retorna todos os relatórios agregados
    incluindo nome da matéria, data da aula e e-mail do professor
    """
    try:
        query = """
            SELECT
                r.report_id,
                r.lecture_id,
                r.subject_id,
                s.name AS subject_name,
                l.date_lecture,
                u.email AS teacher,
                r.total_students,
                r.total_time_watched,
                r.avg_lecture_duration,
                r.avg_idle_duration,
                r.avg_attention_span,
                r.pct_enabled_camera,
                r.pct_enabled_mic,
                r.avg_cam_streaming_span,
                r.avg_mic_streaming_span,
                r.issued_at
            FROM report r
            JOIN lecture l ON r.lecture_id = l.lecture_id
            JOIN subject s ON r.subject_id = s.subject_id
            JOIN users u ON l.teacher_id = u.user_id
            ORDER BY r.issued_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        reports = []

        for row in rows:
            report = Report(
                lecture_id=row[1],
                subject_id=row[2],
                total_students=row[6],
                total_time_watched=row[7],
                avg_lecture_duration=row[8],
                avg_idle_duration=row[9],
                avg_attention_span=row[10],
                pct_enabled_camera=row[11],
                pct_enabled_mic=row[12],
                avg_cam_streaming_span=row[13],
                avg_mic_streaming_span=row[14],
                issued_at=row[15],
                _id=row[0]
            )
            report_dict = report.to_dict()
            report_dict["subject_name"] = row[3]
            report_dict["date_lecture"] = row[4]
            report_dict["teacher"] = row[5]
            reports.append(report_dict)

        return reports

    except Exception as e:
        print("[REPOSITORY] Erro ao buscar reports:", e)
        raise e


def findOneReport(report_id):
    """
    Busca um relatório pelo ID (inclui nome da matéria, data da aula e e-mail do professor)
    """
    try:
        query = """
            SELECT
                r.report_id,
                r.lecture_id,
                r.subject_id,
                s.name AS subject_name,
                l.date_lecture,
                u.email AS teacher,
                r.total_students,
                r.total_time_watched,
                r.avg_lecture_duration,
                r.avg_idle_duration,
                r.avg_attention_span,
                r.pct_enabled_camera,
                r.pct_enabled_mic,
                r.avg_cam_streaming_span,
                r.avg_mic_streaming_span,
                r.issued_at
            FROM report r
            JOIN lecture l ON r.lecture_id = l.lecture_id
            JOIN subject s ON r.subject_id = s.subject_id
            JOIN users u ON l.teacher_id = u.user_id
            WHERE r.report_id = %s
        """
        cursor.execute(query, (report_id,))
        row = cursor.fetchone()

        if not row:
            return None

        report = Report(
            lecture_id=row[1],
            subject_id=row[2],
            total_students=row[6],
            total_time_watched=row[7],
            avg_lecture_duration=row[8],
            avg_idle_duration=row[9],
            avg_attention_span=row[10],
            pct_enabled_camera=row[11],
            pct_enabled_mic=row[12],
            avg_cam_streaming_span=row[13],
            avg_mic_streaming_span=row[14],
            issued_at=row[15],
            _id=row[0]
        )

        extras = {
            "subject_name": row[3],
            "date_lecture": row[4],
            "teacher": row[5]
        }

        return report, extras

    except Exception as e:
        print("[REPOSITORY] Erro ao buscar report:", e)
        raise e


def getReportByLectureId(lecture_id: str):
    """
    Retorna o relatório pelo lecture_id, se existir.
    """
    try:
        query = "SELECT * FROM report WHERE lecture_id = %s"
        cursor.execute(query, (lecture_id,))
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar relatório:", e)
        raise e

def deleteReport(report_id):
    """
    Remove um relatório pelo ID
    """
    try:
        query = "DELETE FROM report WHERE report_id = %s"
        cursor.execute(query, (report_id,))
        conn.commit()
        return {"message": "Relatório removido com sucesso"}
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao remover report:", e)
        raise e

def updateReport(report_id: str, fields: dict):
    """
    Atualiza campos de um relatório existente.
    """
    try:
        if not fields or not isinstance(fields, dict):
            raise ValueError("fields deve ser um dicionário com os campos a atualizar.")

        set_clause = ", ".join([f"{key} = %s" for key in fields.keys()])
        values = list(fields.values()) + [report_id]

        query = f"""
            UPDATE report
            SET {set_clause}
            WHERE report_id = %s
            RETURNING *;
        """

        cursor.execute(query, tuple(values))
        conn.commit()

        updated = cursor.fetchone()
        if updated:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, updated))
        else:
            print(f"[REPOSITORY] Nenhum relatório encontrado com report_id={report_id}.")
            return None

    except Exception as e:
        print("[REPOSITORY] Erro ao atualizar relatório:", e)
        conn.rollback()
        raise e