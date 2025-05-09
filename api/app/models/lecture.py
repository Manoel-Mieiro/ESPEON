from bson import ObjectId


class Lecture():
    def __init__(self, subject: str, period_start: str, period_end: str, teacher: str, _id: ObjectId = None):
        self._id = _id,
        self._subject = subject,
        self._periodStart = period_start,
        self._periodEnd = period_end,
        self._teacher = teacher

    def to_dict(self):
        data = {
            "subject": self._subject,
            "periodStart": self._periodStart,
            "periodEnd": self._periodEnd,
            "teacher": self._teacher
        }
        if self._id:
            data["_id"] = str(self._id)
        return data

    @staticmethod
    def from_dict(data):
        return Lecture(
            subject=data["subject"],
            period_start=data["period_start"],
            period_end=data["period_end"],
            teacher=data["teacher"],
        )
