import uuid
from app.utils.time_utils import convert_time_objects_to_string
from psycopg2.extras import Json
from pg import conn
from app.models.postgres.reports import Report

cursor = conn.cursor()
table = "reports"

def _get_lecture_details(lecture_id: str, subject_id: str):
    """
    Busca o nome da matéria, o email do professor e a data da aula para uma lecture
    """
    try:
        query = """
            SELECT 
                s.name AS subject_name,
                u.email AS teacher_email,
                l.date_lecture  -- Adicionando a data da aula
            FROM lecture l
            JOIN subject s ON l.subject_id = s.subject_id
            JOIN users u ON l.teacher_id = u.user_id
            WHERE l.lecture_id = %s AND s.subject_id = %s
        """
        cursor.execute(query, (lecture_id, subject_id))
        result = cursor.fetchone()
        
        if result:
            return result[0], result[1], result[2] 
        else:
            print(f"[REPOSITORY] Detalhes não encontrados para lecture_id={lecture_id}, subject_id={subject_id}")
            return None, None, None
            
    except Exception as e:
        print(f"[REPOSITORY] Erro ao buscar detalhes da aula: {e}")
        return None, None, None

def createReport(report: Report): 
    try:
        subject_name, teacher_email, date_lecture = _get_lecture_details(report._lecture_id, report._subject_id) 
        
        report_dict = report.to_dict()
        
        report_dict.update({
            "report_id": report._id or str(uuid.uuid4()),
            "subject_name": subject_name,
            "teacher": teacher_email,
            "date_lecture": date_lecture  
        })
        
        report_dict = {k: v for k, v in report_dict.items() if v is not None}
        
        for key, value in report_dict.items():
            if isinstance(value, dict):
                report_dict[key] = Json(value)  # Convert dict to PostgreSQL JSON
                print(f"[DEBUG] Converted {key} to JSON: {value}")
        
        report_dict = convert_time_objects_to_string(report_dict)
            
        columns = ", ".join(report_dict.keys())
        placeholders = ", ".join(["%s"] * len(report_dict))
        values = list(report_dict.values())
        
        query = f"""
            INSERT INTO {table} ({columns})
            VALUES ({placeholders})
            RETURNING report_id;
        """
        
        print("[DEBUG] Executing query...")
        cursor.execute(query, values)
        conn.commit()
        
        result = cursor.fetchone()
        if result:
            print(f"[DEBUG] Report created successfully with ID: {result[0]}")
            return result[0]
        else:
            raise Exception("Falha ao criar relatório - nenhum ID retornado")
        
    except Exception as e:
        print(f"[REPOSITORY] Erro ao criar relatório: {e}")
        conn.rollback()
        raise e

def findAllReports():
    """
    Retorna todos os relatórios com TODOS os campos
    """
    try:
        query = f"""
            SELECT
                r.report_id,
                r.lecture_id,
                r.subject_id,
                r.lecture_alias,
                s.name AS subject_name,
                l.date_lecture,
                u.email AS teacher,
                r.total_students,
                r.lecture_length,
                r.avg_session_per_student,
                r.attendance_ratio,
                r.lecture_focus_ratio,
                r.avg_focus_duration,
                r.max_focus_duration,
                r.distraction_ratio,
                r.distraction_frequency,
                r.main_distractions,
                r.tab_switch_frequency,
                r.multitasking_intensity,
                r.focus_fragmentation,
                r.camera_engagement,
                r.mic_engagement,
                r.voluntary_participation,
                r.engagement_trend,
                r.peak_engagement_time,
                r.dropoff_point,
                r.engagement_score,
                r.attention_health,
                r.distraction_risk,
                r.issued_at
            FROM {table} r
            JOIN lecture l ON r.lecture_id = l.lecture_id
            JOIN subject s ON r.subject_id = s.subject_id
            JOIN users u ON l.teacher_id = u.user_id
            ORDER BY r.issued_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        reports = []
        for row in rows:
            report_data = dict(zip(columns, row))
            report_obj = Report.from_dict(report_data)
            report_dict = report_obj.to_dict()
            reports.append(report_dict)

        return reports

    except Exception as e:
        print("[REPOSITORY] Erro ao buscar reports:", e)
        raise e


def findOneReport(report_id):
    """
    Busca um relatório pelo ID
    """
    try:
        query = f"""
            SELECT
                r.report_id,
                r.lecture_id,
                r.subject_id,
                r.lecture_alias,
                s.name AS subject_name,
                l.date_lecture,
                u.email AS teacher,
                r.total_students,
                r.lecture_length,
                r.avg_session_per_student,
                r.attendance_ratio,
                r.lecture_focus_ratio,
                r.avg_focus_duration,
                r.max_focus_duration,
                r.distraction_ratio,
                r.distraction_frequency,
                r.main_distractions,
                r.tab_switch_frequency,
                r.multitasking_intensity,
                r.focus_fragmentation,
                r.camera_engagement,
                r.mic_engagement,
                r.voluntary_participation,
                r.engagement_trend,
                r.peak_engagement_time,
                r.dropoff_point,
                r.engagement_score,
                r.attention_health,
                r.distraction_risk,
                r.issued_at
            FROM {table} r
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
            lecture_alias=row[3],
            subject_name=row[4],
            date_lecture=row[5],
            teacher=row[6],
            total_students=row[7],
            lecture_length=row[8],
            avg_session_per_student=row[9],
            attendance_ratio=row[10],
            lecture_focus_ratio=row[11],
            avg_focus_duration=row[12],
            max_focus_duration=row[13],
            distraction_ratio=row[14],
            distraction_frequency=row[15],
            main_distractions=row[16],
            tab_switch_frequency=row[17],
            multitasking_intensity=row[18],
            focus_fragmentation=row[19],
            camera_engagement=row[20],
            mic_engagement=row[21],
            voluntary_participation=row[22],
            engagement_trend=row[23],
            peak_engagement_time=row[24],
            dropoff_point=row[25],
            engagement_score=row[26],
            attention_health=row[27],
            distraction_risk=row[28],
            issued_at=row[29],
            _id=row[0]
        )
        extras = {
            "subject_name": row[4], 
            "date_lecture": row[5], 
            "teacher": row[6]       
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
        query = f"""
            SELECT 
                report_id, 
                lecture_id, 
                subject_id,
                lecture_alias,
                subject_name,
                teacher,
                date_lecture,
                total_students,
                lecture_length,
                avg_session_per_student,
                attendance_ratio,
                lecture_focus_ratio,
                avg_focus_duration,
                max_focus_duration,
                distraction_ratio,
                distraction_frequency,
                main_distractions,
                tab_switch_frequency,
                multitasking_intensity,
                focus_fragmentation,
                camera_engagement,
                mic_engagement,
                voluntary_participation,
                engagement_trend,
                peak_engagement_time,
                dropoff_point,
                engagement_score,
                attention_health,
                distraction_risk,
                issued_at
            FROM {table} 
            WHERE lecture_id = %s
        """
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
            raise ValueError(
                "fields deve ser um dicionário com os campos a atualizar.")

        fields_to_update = {k: v for k, v in fields.items() if k not in ['subject_name', 'teacher']}

        print(f"[REPOSITORY] Updating report {report_id}")

        processed_fields = {}
        for key, value in fields_to_update.items():
            if isinstance(value, dict):
                processed_fields[key] = Json(value)
            else:
                processed_fields[key] = value

        set_clause = ", ".join([f"{key} = %s" for key in processed_fields.keys()])
        values = list(processed_fields.values()) + [report_id]

        query = f"""
            WITH updated_report AS (
                UPDATE {table}
                SET {set_clause}
                WHERE report_id = %s
                RETURNING *
            )
            SELECT 
                ur.*,
                s.name AS subject_name,
                u.email AS teacher
            FROM updated_report ur
            JOIN lecture l ON ur.lecture_id = l.lecture_id
            JOIN subject s ON ur.subject_id = s.subject_id
            JOIN users u ON l.teacher_id = u.user_id
        """

        cursor.execute(query, tuple(values))
        conn.commit()

        updated = cursor.fetchone()
        if updated:
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, updated))
            print(f"[REPOSITORY] Update successful")
            
            result = convert_time_objects_to_string(result)
            print(f"[REPOSITORY] After conversion: {result}")
            return result
        else:
            print(
                f"[REPOSITORY] Nenhum relatório encontrado com report_id={report_id}.")
            return None

    except Exception as e:
        print("[REPOSITORY] Erro ao atualizar relatório:", e)
        conn.rollback()
        raise e
