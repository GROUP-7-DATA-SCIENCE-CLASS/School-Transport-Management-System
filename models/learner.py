import re


# ============================== LEARNER ==============================
class Learner:
    """Holds one learner's details. Name, contact and grade are validated by setters."""

    def __init__(self, learner_id, name, grade, contact):
        self._learner_id = learner_id            # protected, read-only
        self.name = name                         # setter validates
        self.contact = contact                   # setter validates
        self.grade = grade                       # setter validates

    VALID_GRADES = ("P1", "P2", "P3", "P4", "P5", "P6", "P7")

    @property
    def learner_id(self):
        return self._learner_id

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        value = str(value).replace(" ", "").upper()
        if value not in self.VALID_GRADES:
            raise ValueError("Grade must be one of: " + ", ".join(self.VALID_GRADES) + ".")
        self._grade = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = " ".join(str(value).split())
        if len(value) < 2 or not all(c.isalpha() or c in " -'." for c in value):
            raise ValueError("Name must have at least 2 characters and contain letters only.")
        self._name = value.title()

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        value = str(value).replace(" ", "")
        if not re.fullmatch(r"0\d{9}|\+256\d{9}", value):
            raise ValueError("Guardian contact must be 10 digits starting with 0 (or +256 and 9 digits).")
        self._contact = value

    def __str__(self):
        return f"{self._learner_id} | {self._name} | {self.grade} | Guardian: {self._contact}"

