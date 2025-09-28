import app.repository.tracesRepository as repository
from app.dto.traces import TracesDTO
import re
from datetime import datetime


def findAllTraces():
    try:
        return repository.findAllTraces()
    except Exception as e:
        print("[SERVICE]Erro ao buscar traces:", e)
        raise e
    
def findOneTraceByLecture(lecture_id):
    try:
        return repository.findOneTraceByLecture(lecture_id)
    except Exception as e:
        print("[SERVICE]Erro ao buscar traces:", e)
        raise e


def createTrace(data: TracesDTO):
    try:
        lecture = extract_lecture_id(data.classTitle)
        data.lectureId = lecture
        timestamp = convertTime(data.timestamp)
        data.timestamp = timestamp
        lastAccessed = convertTime(data.lastAccessed)
        data.lastAccessed = lastAccessed
        return repository.createTrace(data.to_standard())
    except Exception as e:
        print("[SERVICE] Erro ao criar trace:", e)
        raise e


def extractSubject(subject):
    end = subject.index(']')
    substring = subject[1:end]
    return substring.lower().replace(" ", '_')


def extract_lecture_id(title: str) -> str:
    match = re.search(r"\[([^\]]+)\]", title)
    return match.group(1) if match else None


def convertTime(ms: float | int) -> str:
    # converte milissegundos para segundos
    seconds = ms / 1000
    dt = datetime.fromtimestamp(seconds)
    return dt.strftime("%H:%M:%S")
