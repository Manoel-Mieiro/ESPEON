import uuid
from pg import conn
from app.models.postgres.reports import Report

cursor = conn.cursor()


def createReport(report: Report):
    """
    Cria um novo relatório agregado (por aula/disciplina)
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
            RETURNING report_id
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
        report._id = report_id
        return report.to_dict()
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao criar report:", e)
        raise e


def findAllReports():
    """
    Retorna todos os relatórios agregados
    """
    try:
        query = """
            SELECT
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
            FROM report
            ORDER BY issued_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        reports = []

        for row in rows:
            report = Report(
                lecture_id=row[1],
                subject_id=row[2],
                total_students=row[3],
                total_time_watched=row[4],
                avg_lecture_duration=row[5],
                avg_idle_duration=row[6],
                avg_attention_span=row[7],
                pct_enabled_camera=row[8],
                pct_enabled_mic=row[9],
                avg_cam_streaming_span=row[10],
                avg_mic_streaming_span=row[11],
                issued_at=row[12],
                _id=row[0]
            )
            reports.append(report.to_dict())

        return reports
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar reports:", e)
        raise e


def findOneReport(report_id):
    """
    Busca um relatório pelo ID
    """
    try:
        query = """
            SELECT
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
            FROM report
            WHERE report_id = %s
        """
        cursor.execute(query, (report_id,))
        row = cursor.fetchone()

        if not row:
            return None

        report = Report(
            lecture_id=row[1],
            subject_id=row[2],
            total_students=row[3],
            total_time_watched=row[4],
            avg_lecture_duration=row[5],
            avg_idle_duration=row[6],
            avg_attention_span=row[7],
            pct_enabled_camera=row[8],
            pct_enabled_mic=row[9],
            avg_cam_streaming_span=row[10],
            avg_mic_streaming_span=row[11],
            issued_at=row[12],
            _id=row[0]
        )
        return report.to_dict()
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar report:", e)
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
