import app.repository.usersRepository as users


def findAllUsers():
    try:
        return users.findAllUsers()
    except Exception as e:
        print("[SERVICE]Error fetching users:", e)
        raise e


def createUser(data):
    try:
        fetched = findOneUser(data.email)
        if (fetched): raise Exception("Usuário já existe!") 
        return users.createUser(data)
    except Exception as e:
        print("[SERVICE]Error creating user:", e)
        raise e


def findOneUser(user_id=None, email=None):
    try:
        return users.findOneUser(user_id=user_id, email=email)
    except Exception as e:
        print("[SERVICE] Error fetching user:", e)
        raise e



def updateUser(id_user, data):
    try:
        return users.updateUser(id_user, data)
    except Exception as e:
        print("[SERVICE]Error updating user:", e)
        raise e


def deleteUser(id):
    try:
        return users.deleteUser(id)
    except Exception as e:
        print("[SERVICE]Error deleting user:", e)
        raise e
