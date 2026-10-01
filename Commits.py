"""School Transport Management System (lean single-file version).  Run: python school_transport.py"""
import re
from abc import ABC, abstractmethod

# ============================== EXCEPTIONS ==============================
class TransportError(Exception):
    """A business rule of the system was broken."""


class VehicleFullError(TransportError):
    """The vehicle has no free seats."""

# ============================== LEARNER ==============================
class Learner:
    """Holds one learner's details. Name and contact are validated by setters."""

    def __init__(self, learner_id, name, grade, contact):
        self._learner_id = learner_id            # protected, read-only
        self.name = name                         # setter validates
        self.contact = contact                   # setter validates
        if not str(grade).strip():
            raise ValueError("Grade/class cannot be empty.")
        self.grade = str(grade).strip().upper()  # public attribute
    
    @property
    def learner_id(self):
        return self._learner_id

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