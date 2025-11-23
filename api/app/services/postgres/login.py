import app.repository.postgres.loginRepository as login
from app.utils.time_utils import get_current_datetime
from app.utils.logger import auth_logger, db_logger
import string
import random
import datetime
from app.services.email import sendMail


def getToken(user_id, userToken):
    try:
        auth_logger.debug("Service: Buscando token no banco", {'user_id': user_id})
        
        fetched = login.getToken(user_id=user_id)
        
        if not fetched:
            auth_logger.warn("Service: Token não encontrado para usuário", {'user_id': user_id})
            raise ValueError("Invalid token provided.")

        auth_logger.debug("Service: Token encontrado", {
            'user_id': user_id,
            'token_encontrado': fetched.token[:2] + '***' if fetched.token else None,
            'created_at': fetched.created_at
        })

        if fetched.token != userToken:
            auth_logger.warn("Service: Token não corresponde", {
                'user_id': user_id,
                'token_fornecido': userToken[:2] + '***',
                'token_esperado': fetched.token[:2] + '***'
            })
            raise ValueError("Invalid token provided.")

        auth_logger.debug("Service: Validando expiração do token")
        if validateToken(fetched.created_at):
            auth_logger.warn("Service: Token expirado", {
                'user_id': user_id,
                'created_at': fetched.created_at
            })
            return False

        auth_logger.info("Service: Token válido", {'user_id': user_id})
        return True
        
    except Exception as e:
        auth_logger.error("Service: Erro ao validar token", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e


def updateToken(user):
    """
    Gera um novo token para o usuário e envia por email
    """
    try:
        tkn = generateToken()
        generatedAt = get_current_datetime()
        
        auth_logger.debug("Service: Atualizando token no banco", {
            'user_id': user["_id"],
            'email': user["email"],
            'token_gerado': tkn,
            'generated_at': generatedAt
        })

        login.updateToken(user_id=user["_id"], newToken=tkn, created_at=generatedAt)
        
        auth_logger.debug("Service: Enviando token por email", {'email': user["email"]})
        sendMail(user["email"], tkn)

        auth_logger.info("Service: Token atualizado e enviado com sucesso", {
            'user_id': user["_id"],
            'email': user["email"]
        })
        return {"newToken": tkn}
        
    except Exception as e:
        auth_logger.error("Service: Erro ao atualizar token", {
            'user_id': user["_id"],
            'email': user["email"],
            'error': str(e)
        })
        raise


def seedLogin(user):
    """
    Cria o login com token para um usuário já existente
    """
    try:
        auth_logger.debug("Service: Gerando token inicial", {'user_id': user["_id"]})
        
        tkn = generateToken()
        result = login.seedLogin(user_id=user["_id"], token=tkn)
        
        auth_logger.info("Service: Token inicial gerado com sucesso", {
            'user_id': user["_id"],
            'token_gerado': tkn
        })
        return result
        
    except Exception as e:
        auth_logger.error("Service: Erro ao gerar token inicial", {
            'user_id': user["_id"],
            'error': str(e)
        })
        raise e


def deleteToken(user):
    try:
        auth_logger.debug("Service: Removendo token do banco", {'user_id': user["_id"]})
        
        result = login.deleteLogin(user_id=user["_id"])
        
        auth_logger.info("Service: Token removido com sucesso", {'user_id': user["_id"]})
        return result
        
    except Exception as e:
        auth_logger.error("Service: Erro ao remover token", {
            'user_id': user["_id"],
            'error': str(e)
        })
        raise e


def generateToken():
    """
    Gera um token numérico de 6 dígitos
    """
    chars = string.digits
    token = ''.join(random.choice(chars) for i in range(6))
    auth_logger.debug("Service: Token gerado", {'token': token})
    return token


def validateToken(created_at):
    """
    Verifica se o token já expirou (180 segundos)
    """
    lifespan_seconds = 180
    if isinstance(created_at, str):
        created_at = datetime.datetime.fromisoformat(created_at)

    now = get_current_datetime()
    is_expired = now > created_at + datetime.timedelta(seconds=lifespan_seconds)
    
    if is_expired:
        auth_logger.debug("Service: Token expirado", {
            'created_at': created_at,
            'now': now,
            'diferenca_segundos': (now - created_at).total_seconds()
        })
    
    return is_expired