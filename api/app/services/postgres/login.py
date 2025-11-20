import app.repository.postgres.loginRepository as login
from app.utils.time_utils import get_current_datetime
import string
import random
import datetime
from app.services.email import sendMail


def getToken(user_id, userToken):
    try:
        fetched = login.getToken(user_id=user_id)
        print("Fetched token raw:", fetched)
        print("Type:", type(fetched))

        if not fetched or fetched.token != userToken:
            raise ValueError("Invalid token provided.")

        print(f"Validating if token already expired")
        if validateToken(fetched.created_at):
            return False

        print("[SERVICE] Provided Token matches the one assigned to the user")
        return True
    except Exception as e:
        print("[SERVICE] Error fetching token:", e)
        raise e


def updateToken(user):
    """
    Gera um novo token para o usuário e envia por email
    """
    try:
        tkn = generateToken()
        generatedAt = get_current_datetime()
        print("[SERVICE] Token is:", tkn)

        login.updateToken(user_id=user["_id"],
                          newToken=tkn, created_at=generatedAt)
        sendMail(user["email"], tkn)

        return {"newToken": tkn}
    except Exception as e:
        print("[SERVICE] Error updating user token:", e)
        raise


def seedLogin(user):
    """
    Cria o login com token para um usuário já existente
    """
    try:
        print("[SERVICE] Generating token...")
        tkn = generateToken()
        return login.seedLogin(user_id=user["_id"], token=tkn)
    except Exception as e:
        print("[SERVICE] Error assigning token to user:", e)
        raise e


def deleteToken(user):
    try:
        return login.deleteLogin(user_id=user["_id"])
    except Exception as e:
        print("[SERVICE] Error deleting user token:", e)
        raise e


def generateToken():
    """
    Gera um token numérico de 6 dígitos
    """
    chars = string.digits
    return ''.join(random.choice(chars) for i in range(6))


def validateToken(created_at):
    """
    Verifica se o token já expirou (180 segundos)
    """
    lifespan_seconds = 180
    if isinstance(created_at, str):
        created_at = datetime.datetime.fromisoformat(created_at)

    now = get_current_datetime()
    return now > created_at + datetime.timedelta(seconds=lifespan_seconds)
