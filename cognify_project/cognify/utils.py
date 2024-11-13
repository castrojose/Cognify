# cognify/utils.py

from .models import Memory, CrimeType

class SimulationConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationConfig, cls).__new__(cls)
            cls._instance.config = {}
        return cls._instance

class MemoryBuilder:
    def __init__(self):
        self.memory = Memory()

    def set_description(self, description):
        self.memory.description = description
        return self

    def set_impact_level(self, impact_level):
        self.memory.impact_level = impact_level
        return self

    def set_duration(self, duration):
        self.memory.duration = duration
        return self

    def build(self):
        return self.memory
