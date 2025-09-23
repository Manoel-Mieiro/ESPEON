import uuid
from app.models.roles import Roles
from pg import conn
from app.models.postgres.users import Users

cursor = conn.cursor()


def findAllUsers():
    try:
        cursor.execute("SELECT user_id, email, role FROM users;")
        rows = cursor.fetchall()
        users_list = []

        for row in rows:
            user = Users(
                user_id=row[0],
                email=row[1],
                role=row[2]
            )
            users_list.append(user.to_dict())

        return users_list

    except Exception as e:
        print("[REPOSITORY] Erro ao buscar users:", e)
        raise e


def createUser(data: Users):
    try:
        print("\n[REPOSITORY] Criando user:", data, "\n")
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (user_id, email, role) VALUES (%s, %s, %s);",
            (user_id, data.email, data.role.value)
        )
        conn.commit()

        data.user_id = user_id

        # Criar login
        cursor.execute(
            "INSERT INTO login (login_id, user_id, token, created_at) VALUES (%s, %s, %s, %s);",
            (str(uuid.uuid4()), data.user_id, None, None)
        )
        conn.commit()


        return data.to_dict()

    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao criar user:", e)
        raise e


def findOneUser(user_id=None, email=None):
    try:
        if email:
            cursor.execute(
                "SELECT user_id, email, role FROM users WHERE email=%s;", (email,))
        elif user_id:
            cursor.execute(
                "SELECT user_id, email, role FROM users WHERE user_id=%s;", (user_id,))
        else:
            return None

        row = cursor.fetchone()
        if not row:
            return None

        # Converte role string para enum
        role = Roles(row[2]) if isinstance(row[2], str) else row[2]

        user = Users(
            user_id=row[0],
            email=row[1],
            role=role
        )
        return user.to_dict()
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar user:", e)
        raise e



def updateUser(user_id: str, updatedUser: dict):
    try:
        set_clause = ", ".join([f"{k}=%s" for k in updatedUser.keys()])
        values = list(updatedUser.values()) + [user_id]

        cursor.execute(
            f"UPDATE users SET {set_clause} WHERE user_id=%s RETURNING user_id, email, role;",
            values
        )
        row = cursor.fetchone()
        conn.commit()

        if not row:
            raise ValueError("Usuário não encontrado.")

        return Users(user_id=row[0], email=row[1], role=row[2]).to_dict()

    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao atualizar user:", e)
        raise e


def deleteUser(user_id: str):
    try:
        user = findOneUser(user_id=user_id)
        if not user:
            raise ValueError(f"Usuário {user_id} não encontrado.")

        # Deletar login
        cursor.execute("DELETE FROM login WHERE email=%s;", (user["email"],))
        conn.commit()

        # Deletar usuário
        cursor.execute("DELETE FROM users WHERE id=%s;", (user_id,))
        conn.commit()

        return {"message": "[REPOSITORY] Usuário removido com sucesso"}

    except Exception as e:
        conn.rollback()
        print("[REPOSITORY] Erro ao remover user:", e)
        raise e
