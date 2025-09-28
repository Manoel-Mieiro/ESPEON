from app.models.users import Users
from app.models.roles import Roles
from typing import Optional
import uuid


class UserDTO:
    def __init__(self, email: str, role: str, user_id: Optional[str] = None):
        self.user_id = user_id  # UUID opcional
        self.email = email
        self.role = role

    def to_standard(self):
        """
        Converte o DTO para o modelo Users compatível com o repositório
        """
        return Users(
            _id=self.user_id or str(uuid.uuid4()),  # Gera UUID se não existir
            email=self.email,
            role=Roles(self.role)  # Assumindo que Roles aceita string
        )
