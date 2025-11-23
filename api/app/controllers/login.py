import app.services.postgres.login as loginService
from app.dto.postgres.users import UserDTO
from app.utils.logger import auth_logger


def getToken(user_id, userToken):
    """
    Verifica se o token do usuário é válido
    """
    try:
        auth_logger.debug("Controller: Validando token", {
            'user_id': user_id,
            'token_length': len(userToken) if userToken else 0
        })
        
        result = loginService.getToken(user_id=user_id, userToken=userToken)
        
        auth_logger.debug("Controller: Resultado da validação", {
            'user_id': user_id,
            'valid': result
        })
        return result
        
    except Exception as e:
        auth_logger.error("Controller: Erro ao validar token", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e


def updateToken(user):
    """
    Gera um novo token para o usuário e envia por email
    """
    try:
        auth_logger.debug("Controller: Gerando novo token", {
            'user_id': user.get("_id"),
            'email': user.get("email")
        })
        
        result = loginService.updateToken(user=user)
        
        auth_logger.info("Controller: Token gerado com sucesso", {
            'user_id': user.get("_id"),
            'email': user.get("email")
        })
        return result
        
    except Exception as e:
        auth_logger.error("Controller: Erro ao gerar token", {
            'user_id': user.get("_id"),
            'email': user.get("email"),
            'error': str(e)
        })
        raise e


def deleteToken(user_id):
    """
    Remove o token do usuário
    """
    try:
        auth_logger.debug("Controller: Removendo token", {'user_id': user_id})
        
        result = loginService.deleteToken(user_id=user_id)
        
        auth_logger.info("Controller: Token removido com sucesso", {'user_id': user_id})
        return result
        
    except Exception as e:
        auth_logger.error("Controller: Erro ao remover token", {
            'user_id': user_id,
            'error': str(e)
        })
        raise e