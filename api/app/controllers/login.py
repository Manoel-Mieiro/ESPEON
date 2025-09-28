import app.services.postgres.login as loginService
from app.dto.postgres.users import UserDTO


def getToken(user_id, userToken):
    """
    Verifica se o token do usuário é válido
    """
    try:
        print("[CONTROLLER]user_id:", user_id)
        print("[CONTROLLER]userToken:", userToken)
        return loginService.getToken(user_id=user_id, userToken=userToken)
    except Exception as e:
        print("[CONTROLLER] Error fetching token:", e)
        raise e


def updateToken(user):
    """
    Gera um novo token para o usuário e envia por email
    """
    try:
        return loginService.updateToken(user=user)
    except Exception as e:
        print("[CONTROLLER] Error updating token:", e)
        raise e


def deleteToken(user_id):
    """
    Remove o token do usuário
    """
    try:
        return loginService.deleteToken(user_id=user_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting token:", e)
        raise e
