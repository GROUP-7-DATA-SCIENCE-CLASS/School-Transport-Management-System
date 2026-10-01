"""School Transport Management System (lean single-file version).  Run: python school_transport.py"""
import re
from abc import ABC, abstractmethod

# ============================== EXCEPTIONS ==============================
class TransportError(Exception):
    """A business rule of the system was broken."""


class VehicleFullError(TransportError):
    """The vehicle has no free seats."""
