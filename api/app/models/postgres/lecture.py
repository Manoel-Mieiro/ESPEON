import uuid
from datetime import date, time

class Lecture:
    def __init__(
        self,
        subject_id: str,
        teacher_id: str,
        date_lecture: date,
        period_start: str,
        period_end: str,
        lecture_id: str = None
    ):
        """
        :param subject_id: UUID da disciplina
        :param teacher_id: UUID do professor
        :param date_lecture: data da aula
        :param period_start: horário de início (time)
        :param period_end: horário de término (time)
        :param lecture_id: UUID da aula (opcional, será gerado se não fornecido)
        """
        self.lecture_id = lecture_id or str(uuid.uuid4())
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.date_lecture = date_lecture
        self.period_start = period_start
        self.period_end = period_end

    def to_dict(self):
        """
        Converte a aula para dicionário para persistência ou JSON
        """
        return {
            "lecture_id": self.lecture_id,
            "subject_id": self.subject_id,
            "teacher_id": self.teacher_id,
            "date_lecture": self.date_lecture,
            "period_start": self.period_start,
            "period_end": self.period_end
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Cria uma instância de Lecture a partir de um dicionário
        """
        return Lecture(
            lecture_id=data.get("lecture_id"),
            subject_id=data["subject_id"],
            teacher_id=data["teacher_id"],
            date_lecture=data["date_lecture"],
            period_start=data["period_start"],
            period_end=data["period_end"]
        )

    def __str__(self):
        return f"Lecture({self.lecture_id}): {self.subject_id} - {self.teacher_id} on {self.date_lecture}"
