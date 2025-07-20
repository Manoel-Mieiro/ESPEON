import app.services.traces as traceService
from app.dto.traces import TracesDTO


def listTraces(subject):
    try:
        return traceService.findAllTraces(subject)
    except Exception as e:
        print("[CONTROLLER]Error fetching traces:", e)
        raise e


def createTrace(data):
    try:
        print("\n[CONTROLLER]Payload recebido:", data)
        dto = TracesDTO(**data)
        trace = dto.to_standard()
        return traceService.createTrace(trace)
    except Exception as e:
        print("[CONTROLLER]Error creating trace:", e)
        raise e
