import uuid
from pg import conn
from app.models.postgres.login import Login
from app.utils.logger import db_logger

cursor = conn.cursor()


def seedLogin(user_id: str, token: str):
    """
    Cria um login associado a um usuário com UUID user_id
    """
    try:
        db_logger.debug("Repository: Criando login inicial", {
            'user_id': user_id,
            'token_length': len(token)
        })
        
        login_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO login (login_id, user_id, token) VALUES (%s, %s, %s);",
            (login_id, user_id, token)
        )
        conn.commit()
        
        db_logger.info("Repository: Login criado com sucesso", {
            'login_id': login_id,
            'user_id': user_id
        })
        return True
        
    except Exception as e:
        conn.rollback()
        db_logger.error("Repository: Erro ao criar login", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e


def getToken(user_id: str):
    """
    Retorna o login do usuário pelo user_id
    """
    try:
        db_logger.debug("Repository: Buscando token", {'user_id': user_id})

        cursor.execute(
            "SELECT login_id, user_id, token, created_at FROM login WHERE user_id=%s;",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            db_logger.debug("Repository: Nenhum token encontrado", {'user_id': user_id})
            return None

        login_dict = {
            "_id": row[0],
            "user_id": row[1],
            "token": row[2],
            "created_at": row[3],
        }

        db_logger.debug("Repository: Token encontrado", {
            'user_id': user_id,
            'login_id': login_dict["_id"],
            'created_at': login_dict["created_at"]
        })

        return Login.from_dict(login_dict)

    except Exception as e:
        db_logger.error("Repository: Erro ao buscar token", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e


def updateToken(user_id: str, newToken: str, created_at):
    """
    Atualiza token e created_at para o login de um usuário
    """
    try:
        db_logger.debug("Repository: Atualizando token", {
            'user_id': user_id,
            'new_token': newToken,
            'created_at': created_at
        })
        
        cursor.execute(
            "UPDATE login SET token=%s, created_at=%s WHERE user_id=%s RETURNING login_id;",
            (newToken, created_at, user_id)
        )
        row = cursor.fetchone()
        conn.commit()

        if not row:
            db_logger.error("Repository: Usuário não encontrado para atualização", {'user_id': user_id})
            raise ValueError(f"Não foi possível atualizar o token para {user_id}: Usuário não encontrado.")

        db_logger.info("Repository: Token atualizado com sucesso", {
            'user_id': user_id,
            'login_id': row[0]
        })
        return newToken
        
    except Exception as e:
        conn.rollback()
        db_logger.error("Repository: Erro ao atualizar token", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e


def deleteLogin(user_id: str):
    """
    Deleta login de um usuário
    """
    try:
        db_logger.debug("Repository: Deletando login", {'user_id': user_id})
        
        cursor.execute(
            "DELETE FROM login WHERE user_id=%s RETURNING login_id;",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.commit()

        if not row:
            db_logger.warn("Repository: Login não encontrado para deleção", {'user_id': user_id})
            raise ValueError("Usuário não encontrado.")

        db_logger.info("Repository: Login deletado com sucesso", {
            'user_id': user_id,
            'login_id_deletado': row[0]
        })

    except Exception as e:
        conn.rollback()
        db_logger.error("Repository: Erro ao deletar login", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e