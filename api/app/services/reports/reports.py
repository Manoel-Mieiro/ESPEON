import app.repository.reportRepository as repository
collection = None

def findAllReports(kind):
    try:
        return repository.findAllReports(kind)
    except Exception as e:
        print("[SERVICE]Erro ao buscar reports:", e)
        raise e


def createReport(data, kind):
    try:
        print("[SERVICE]Criando report:", data)
        return repository.createReport(data, kind)
    except Exception as e:
        print("[SERVICE]Erro ao criar report:", e)
        raise e


def extractSubject(subject):
    end = subject.index(']')
    substring = subject[1:end]
    return substring.lower().replace(" ", '_')
