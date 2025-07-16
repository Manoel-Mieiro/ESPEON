import app.repository.lecturesRepository2 as lectures

def findAllLectures():
    try:
        return lectures.findAllLectures()
    except Exception as e:
        print("[SERVICE]Error fetching lectures:", e)
        raise e
    