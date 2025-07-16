from bson import ObjectId
from db import client
from app.models.lecture import Lecture

db = client["TRACES"]
lectures = db["lectures"]

def findAllLectures():
    try:
        docs = list(lectures.find({}))
        lectures_list = []

        for doc in docs:
            lecture = Lecture.from_dict(doc)
            lectures_list.append(lecture.to_dict())

        return lectures_list

    except Exception as e:
        print("[REPOSITORY]Erro ao buscar aulas:", e)
        raise e


def findOneLecture(_id):
    try:
        objectId = ObjectId(_id)
        lecture_data = lectures.find_one({"_id": objectId})
        if not lecture_data:
            return None

        return Lecture.from_dict(lecture_data).to_dict()
    except Exception as e:
        print(f"[REPOSITORY]Erro ao buscar aula:", e)
        raise e


def createLecture(data: Lecture):
    try:
        print("\n[REPOSITORY]Criando aula:", data.to_dict(), "\n")
        result = lectures.insert_one(data.to_dict())
        data._id = result.inserted_id

        if not data._id:
            raise Exception("Erro ao inserir aula no banco.")

        return data.to_dict()
    except Exception as e:
        print("[REPOSITORY]Erro ao criar lecture:", e)
        raise e


def updateLecture(_id: ObjectId, updatedLecture: dict):
    try:
        result = lectures.update_one(
            {"_id": ObjectId(_id)},
            {"$set": updatedLecture}
        )

        if result.matched_count == 0:
            raise ValueError("Usuário não encontrado.")

        return findOneLecture(_id)
    except Exception as e:
        print("[REPOSITORY]Erro ao atualizar lecture:", e)
        raise e


def deleteLecture(_id: str):
    try:
        objectId = ObjectId(_id)
        lecture = lectures.find_one({"_id": objectId})

        if not lecture:
            raise ValueError(f"[REPOSITORY]Aula {_id} não encontrado")

        result = lectures.delete_one({"_id": objectId})

        if result.deleted_count == 0:
            raise ValueError(f"[REPOSITORY]Erro ao remover aula {_id}")
        return {"message": "[REPOSITORY]Aula removida com sucesso"}
    except Exception as e:
        print("[REPOSITORY]Erro ao remover aula:", e)
        raise e
