from bson import ObjectId
from db import client
from app.models.login import Login

db = client["TRACES"]
login = db["login"]

def seedLogin(usr, token):
    try:
        print("\n[REPOSITORY]Atribuindo token ao usuário:", usr, "\n")
        login.insert_one(Login(usr, token=token))
        return True
    except Exception as e:
        print("[REPOSITORY] Erro inesperado no getToken: ", e)
        raise e


def getToken(usr):
    try:
        data = login.find_one({"email": usr})
        if not data:
            return None

        return Login.from_dict(data)
    except Exception as e:
        print("[REPOSITORY] Erro inesperado no getToken: ", e)
        raise e


def updateToken(email: str, newToken: str, createdAt):
    try:
        association = login.find_one({"email": email})
        if not association:
            raise ValueError(
                f"Não foi possível atualizar o token para {email}: Usuário não encontrado.")

        result = login.update_one(
            {"email": email},
            {"$set": {"token": newToken, "createdAt": createdAt}}
        )

        if result.modified_count == 0:
            raise ValueError(
                f"Token não foi atualizado para {email}. Talvez o token enviado seja o mesmo.")

        return newToken
    except Exception as e:
        print("[REPOSITORY]Erro ao atualizar token:", e)
        raise e


def deleteLogin(usr: Login):
    try:
        result = login.delete_one(
            {"email": usr.email}
        )
        if result.deleted_count == 0:
            raise ValueError(f"Usuário não encontrado")
    except Exception as e:
        print("[REPOSITORY] Erro inesperado: ", e)
        raise e
