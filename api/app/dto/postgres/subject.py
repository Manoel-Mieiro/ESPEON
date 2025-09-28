class SubjectDTO:
    def __init__(self, name: str, subject_id: str = None):
        self.subject_id = subject_id
        self.name = name

    def to_standard(self):
        """
        Retorna um dicionário padrão para inserção/atualização no serviço/repositório
        """
        return {
            "subject_id": self.subject_id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um SubjectDTO a partir de um dicionário
        """
        return cls(
            name=data.get("name"),
            subject_id=data.get("subject_id")
        )
