import app.services.traces as traceService
from app.dto.traces import TracesDTO


def listTraces():
    try:
        return traceService.findAllTraces()
    except Exception as e:
        print("[CONTROLLER]Error fetching traces:", e)
        raise e
    
def findOneTraceByLecture(lecture_id):
    try:
        return traceService.findOneTraceByLecture(lecture_id)
    except Exception as e:
        print("[CONTROLLER]Error fetching traces:", e)
        raise e

def createTrace(data):
    try:
        print("\n[CONTROLLER]Payload recebido:", data)
        dto = TracesDTO(**data)
        return traceService.createTrace(dto)
    except Exception as e:
        print("[CONTROLLER]Error creating trace:", e)
        raise e
