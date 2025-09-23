from app.models.roles import Roles
from typing import Optional


class Users:
    def __init__(self, email: str, role: Roles, user_id: Optional[str] = None):
        """
        :param email: Email do usuário
        :param role: Instância de Roles (enum)
        :param user_id: UUID do usuário como string (opcional)
        """
        self.user_id = user_id  # UUID como string
        self.email = email
        self.role = role

    def __str__(self):
        return f"[{self.role.value}]: {self.email}"

    def to_dict(self):
        """
        Converte o objeto Users em dicionário para persistência ou JSON
        """
        data = {
            "email": self.email,
            "role": self.role.value if isinstance(self.role, Roles) else self.role
        }
        if self.user_id:
            data["user_id"] = self.user_id
        return data

    @staticmethod
    def from_dict(data: dict):
        """
        Cria um objeto Users a partir de um dicionário
        """
        if "email" not in data or "role" not in data:
            raise ValueError(f"Documento inválido, campos ausentes: {data}")

        # Converte string para enum se necessário
        role_value = data["role"]
        if isinstance(role_value, str):
            role_value = Roles(role_value)
    
        return Users(
            email=data["email"],
            role=role_value,
            user_id=data.get("user_id")  # Agora espera string UUID
        )
