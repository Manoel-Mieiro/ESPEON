import app.repository.postgres.loginRepository as login
from app.utils.time_utils import get_current_datetime
from app.utils.logger import auth_logger, db_logger
import string
import random
import datetime
import time
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
    user_id = user["_id"]
    user_email = user["email"]
    
    try:
        auth_logger.info("Service: Iniciando atualização de token", {
            'user_id': user_id,
            'email': user_email,
            'operation': 'token_update_start'
        })
        
        auth_logger.debug("Service: Gerando novo token", {
            'user_id': user_id,
            'email': user_email
        })
        
        tkn = generateToken()
        generatedAt = get_current_datetime()
        
        token_preview = f"{tkn[:8]}..." if len(tkn) > 8 else tkn
        auth_logger.debug("Service: Token gerado com sucesso", {
            'user_id': user_id,
            'email': user_email,
            'token_preview': token_preview,
            'token_length': len(tkn),
            'generated_at': generatedAt
        })

        auth_logger.debug("Service: Atualizando token no banco de dados", {
            'user_id': user_id,
            'email': user_email,
            'operation': 'database_update'
        })
        
        login.updateToken(user_id=user_id, newToken=tkn, created_at=generatedAt)
        
        auth_logger.info("Service: Token atualizado no banco com sucesso", {
            'user_id': user_id,
            'email': user_email
        })

        auth_logger.debug("Service: Preparando envio de email", {
            'user_id': user_id,
            'email': user_email,
            'operation': 'email_preparation'
        })
        
        email_start_time = time.time()
        
        try:
            sendMail(user_email, tkn)
            email_duration = round((time.time() - email_start_time) * 1000, 2)  # em ms
            
            auth_logger.email_operation(
                operation="send_token",
                recipient=user_email,
                status="success",
                subject="Token de Acesso",
                duration=email_duration,
                email_type="authentication"
            )
            
            auth_logger.info("Service: Token enviado por email com sucesso", {
                'user_id': user_id,
                'email': user_email,
                'email_duration_ms': email_duration
            })
            
        except Exception as email_error:
            email_duration = round((time.time() - email_start_time) * 1000, 2)
            
            auth_logger.email_operation(
                operation="send_token",
                recipient=user_email,
                status="error",
                subject="Token de Acesso",
                duration=email_duration,
                error=str(email_error),
                email_type="authentication"
            )
            
            auth_logger.error("Service: Erro no envio do email", {
                'user_id': user_id,
                'email': user_email,
                'error': str(email_error),
                'email_duration_ms': email_duration
            })
            raise email_error

        auth_logger.info("Service: Processo de atualização de token concluído com sucesso", {
            'user_id': user_id,
            'email': user_email,
            'token_generated_at': generatedAt,
            'total_operation': 'token_update_complete'
        })
        
        return {"newToken": tkn}
        
    except Exception as e:
        auth_logger.error("Service: Erro geral no processo de atualização de token", {
            'user_id': user_id,
            'email': user_email,
            'error_type': type(e).__name__,
            'error_message': str(e),
            'operation': 'token_update_failed'
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