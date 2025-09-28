import app.repository.postgres.usersRepository as users


def findAllUsers():
    try:
        return users.findAllUsers()
    except Exception as e:
        print("[SERVICE] Error fetching users:", e)
        raise e


def createUser(data):
    try:
        # Verifica se o usuário já existe pelo email
        fetched = findOneUser(data.email)
        if fetched:
            raise Exception("Usuário já existe!") 
        return users.createUser(data)
    except Exception as e:
        print("[SERVICE] Error creating user:", e)
        raise e


def findOneUser(email=None, user_id=None):
    try:
        # Busca por email ou UUID
        return users.findOneUser(user_id=user_id, email=email)
    except Exception as e:
        print("[SERVICE] Error fetching user:", e)
        raise e


def updateUser(user_id, data):
    try:
        return users.updateUser(user_id, data)
    except Exception as e:
        print("[SERVICE] Error updating user:", e)
        raise e


def deleteUser(user_id):
    try:
        return users.deleteUser(user_id)
    except Exception as e:
        print("[SERVICE] Error deleting user:", e)
        raise e
