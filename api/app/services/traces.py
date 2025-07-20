import app.repository.tracesRepository as repository

collection = None

def findAllTraces(subject):
    try:
        return repository.findAllTraces(subject)
    except Exception as e:
        print("[SERVICE]Erro ao buscar traces:", e)
        raise e


def createTrace(data):
    try:
        print("[SERVICE]Definindo Collection...")
        collection = extractSubject(data.classTitle)
        print("[SERVICE]Collection: ", collection)
        print("[SERVICE]Criando trace:", data)
        return repository.createTrace(data, collection)
    except Exception as e:
        print("[SERVICE]Erro ao criar trace:", e)
        raise e


def extractSubject(subject):
    end = subject.index(']')
    substring = subject[1:end]
    return substring.lower().replace(" ", '_')


# def convertObjectIdToString(json):
#     try:
#         if isinstance(json, list):
#             for item in json:
#                 if '_id' in item:
#                     item['_id'] = str(item['_id'])
#         elif isinstance(json, dict):
#             if '_id' in json:
#                 json['_id'] = str(json['_id'])
#         return json
#     except Exception as e:
#         print("[SERVICE]Erro ao converter ObjectId para string:", e)
#         raise e
