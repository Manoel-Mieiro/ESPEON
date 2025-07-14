from bson import ObjectId
from db import client
from app.models.traces import Traces

db = client["TRACES"]
traces = db["dummy2"]

def findAllTraces():
    try:
        docs = list(traces.find({}))
        trace_list = []

        for doc in docs:
            trace = Traces.from_dict(doc)
            trace_list.append(trace.to_dict())

        return trace_list

    except Exception as e:
        print("[REPOSITORY]Erro ao buscar traces:", e)
        raise e


def createTrace(data: Traces):
    try:
        print("\n[REPOSITORY]Criando trace:", data, "\n")
        result = traces.insert_one(data.to_dict())
        data._id = result.inserted_id

        if not data._id:
            raise Exception("Erro ao inserir trace no banco.")

        return data.to_dict()
    except Exception as e:
        print("[REPOSITORY]Erro ao criar trace:", e)
        raise e
