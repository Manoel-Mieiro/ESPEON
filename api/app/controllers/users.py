import app.services.postgres.users as userService
from app.dto.postgres.users import UserDTO


def findAllUsers():
    try:
        return userService.findAllUsers()
    except Exception as e:
        print("[CONTROLLER]Error fetching users:", e)
        raise e


def createUser(data):
    try:
        user = UserDTO(
            email=data["email"],
            role=data["role"]
        )
        return userService.createUser(user.to_standard())
    except Exception as e:
        print("[CONTROLLER]Error creating user:", e)
        raise e


def findOneUser(email):
    try:
        return userService.findOneUser(email)
    except Exception as e:
        print("[CONTROLLER]Error fetching user:", e)
        raise e


def updateUser(id_user, updatedUser):
    try:
        return userService.updateUser(id_user, updatedUser)
    except Exception as e:
        print("[CONTROLLER]Error updationg user:", e)
        raise e


def deleteUser(id_user):
    try:
        return userService.deleteUser(id_user)
    except Exception as e:
        print("[CONTROLLER]Error deleting user:", e)
        raise e
