import app.services.lectures2 as lectureService


def findAllLectures():
    try:
        return lectureService.findAllLectures()
    except Exception as e:
        print("[CONTROLLER]Error fetching lectures:", e)
        raise e
