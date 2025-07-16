from db import client
db = client["SUBJECT"]

def findAllLectures():
        try:
              collections = db.list_collection_names()
              return collections
        except Exception as e:
            print("[REPOSITORY]Erro ao buscar aulas:", e)
        raise e