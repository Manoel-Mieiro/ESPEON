from typing import Optional


class Subject:
    def __init__(self, name: str, subject_id: Optional[str] = None):
        """
        :param name: Nome da disciplina
        :param subject_id: UUID da disciplina (opcional)
        """
        self.subject_id = subject_id
        self.name = name

    def __str__(self):
        return f"[{self.subject_id}]: {self.name}"

    def to_dict(self):
        """
        Converte o objeto Subject em dicionário para persistência ou JSON
        """
        data = {
            "name": self.name
        }
        if self.subject_id:
            data["subject_id"] = self.subject_id
        return data

    @staticmethod
    def from_dict(data: dict):
        """
        Cria um objeto Subject a partir de um dicionário
        """
        if "name" not in data:
            raise ValueError(f"Documento inválido, campo ausente: {data}")

        return Subject(
            name=data["name"],
            subject_id=data.get("subject_id")
        )

    @classmethod
    def from_row(cls, row: tuple):
        """
        Cria um objeto Subject a partir de uma tupla do banco (subject_id, name)
        """
        if not row or len(row) < 2:
            raise ValueError(f"Row inválida: {row}")
        return cls(subject_id=row[0], name=row[1])
