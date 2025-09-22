import uuid
from pg import conn
from app.models.postgres.login import Login

cursor = conn.cursor()


def seedLogin(user_id: str, token: str):
    """
    Cria um login associado a um usuário com UUID user_id
    """
    try:
        print(f"\n[REPOSITORY] Atribuindo token ao usuário: {user_id}\n")
        login_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO login (login_id, user_id, token) VALUES (%s, %s, %s);",
            (login_id, user_id, token)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro inesperado no seedLogin:", e)
        raise e


def getToken(user_id: str):
    """
    Retorna o login do usuário pelo user_id
    """
    try:
        print(f"[REPOSITORY] getToken chamado com user_id: {user_id}")

        cursor.execute(
            "SELECT login_id, user_id, token, created_at FROM login WHERE user_id=%s;",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            print(f"[REPOSITORY] Nenhum registro encontrado para user_id: {user_id}")
            return None

        login_dict = {
            "_id": row[0],
            "user_id": row[1],
            "token": row[2],
            "created_at": row[3],
        }

        print(f"[REPOSITORY] Registro encontrado: {login_dict}")

        return Login.from_dict(login_dict)
        # return 1

    except Exception as e:
        print("[REPOSITORY] Erro inesperado no getToken:", e)
        raise e



def updateToken(user_id: str, newToken: str, created_at):
    """
    Atualiza token e created_at para o login de um usuário
    """
    try:
        cursor.execute(
            "UPDATE login SET token=%s, created_at=%s WHERE user_id=%s RETURNING login_id;",
            (newToken, created_at, user_id)
        )
        row = cursor.fetchone()
        conn.commit()

        if not row:
            raise ValueError(f"Não foi possível atualizar o token para {user_id}: Usuário não encontrado.")

        return newToken
    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao atualizar token:", e)
        raise e


def deleteLogin(user_id: str):
    """
    Deleta login de um usuário
    """
    try:
        cursor.execute(
            "DELETE FROM login WHERE user_id=%s RETURNING login_id;",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.commit()

        if not row:
            raise ValueError("Usuário não encontrado.")

    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro inesperado no deleteLogin:", e)
        raise e
