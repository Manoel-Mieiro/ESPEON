from bson import ObjectId
from db import client
from app.models.traces import Traces

db = client["TRACES"]
collection = "logs"


def findAllTraces():
    """Busca todos os traces da collection logs."""
    try:
        docs = list(db[collection].find({}))
        trace_list = [Traces.from_dict(doc).to_dict() for doc in docs]
        return trace_list
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar traces:", e)
        raise e


def findOneTraceByLecture(lecture_id: str):
    """Busca todos os traces na collection logs pelo lecture_id."""
    try:
        docs = list(db[collection].find({"lectureId": lecture_id}))
        if not docs:
            return []
        trace_list = [Traces.from_dict(doc).to_dict() for doc in docs]
        return trace_list
    except Exception as e:
        print("[REPOSITORY] Erro ao buscar traces por lecture_id:", e)
        raise e


def createTrace(data: Traces):
    """Cria um trace na collection logs."""
    try:
        print("\n[REPOSITORY] Criando trace:", data, "\n")
        result = db[collection].insert_one(data.to_dict())
        data._id = result.inserted_id

        if not data._id:
            raise Exception("Erro ao inserir trace no banco.")

        return data.to_dict()
    except Exception as e:
        print("[REPOSITORY] Erro ao criar trace:", e)
        raise e
