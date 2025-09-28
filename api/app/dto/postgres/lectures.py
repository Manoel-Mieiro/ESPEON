from app.models.postgres.lecture import Lecture
from datetime import datetime, date, time


class LectureDTO:
    def __init__(
        self,
        subject_id: str,
        teacher_id: str,
        date_lecture: str,
        period_start: str,
        period_end: str
    ):
        """
        :param subject_id: UUID da disciplina
        :param teacher_id: UUID do professor
        :param date_lecture: string no formato 'YYYY-MM-DD'
        :param period_start: string no formato 'HH:MM'
        :param period_end: string no formato 'HH:MM'
        """
        if not subject_id or not teacher_id or not date_lecture or not period_start or not period_end:
            raise ValueError("All fields are required")

        self.subject_id = subject_id
        self.teacher_id = teacher_id
        # Converte strings para tipos nativos
        self.date_lecture = datetime.strptime(date_lecture, "%Y-%m-%d").date()
        self.period_start = period_start
        self.period_end = period_end

    def to_standard(self):
        """
        Converte para o modelo Lecture do Postgres
        """
        return Lecture(
            subject_id=self.subject_id,
            teacher_id=self.teacher_id,
            date_lecture=self.date_lecture,
            period_start=self.period_start,
            period_end=self.period_end
        )
