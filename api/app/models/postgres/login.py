from app.utils.time_utils import get_current_datetime
from typing import Optional
import datetime


class Login:
    def __init__(self, user_id: str, token: str, created_at: Optional[datetime.datetime] = None, login_id: Optional[str] = None):
        """
        :param user_id: UUID do usuário
        :param token: Token de autenticação
        :param created_at: Timestamp da criação do token
        :param login_id: UUID do login (opcional)
        """
        self.login_id = login_id  # UUID do login
        self.user_id = user_id    # UUID do usuário
        self.token = token
        self.created_at = created_at or get_current_datetime()

    def to_dict(self):
        """
        Converte o objeto Login em dicionário para persistência ou JSON
        """
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at
        }
        if self.login_id:
            data["login_id"] = self.login_id
        return data

    @staticmethod
    def from_dict(data: dict):
        """
        Cria um objeto Login a partir de um dicionário
        """
        return Login(
            user_id=data["user_id"],
            token=data["token"],
            created_at=data.get("created_at"),
            login_id=data.get("login_id")
        )
