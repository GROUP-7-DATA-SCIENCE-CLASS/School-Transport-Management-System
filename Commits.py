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