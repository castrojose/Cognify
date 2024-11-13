# cognify/utils.py

from .models import Memory, CrimeType
import random

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

# New function to generate a positive memory
def generate_memory(prompt):
    # For this example, the prompt might not be used, but you could use AI models or predefined templates to generate the memory
    memory_description = "Recuerdo positivo de la infancia: " + random.choice([
        "Jugando con amigos en el parque.",
        "Disfrutando de una tarde soleada con la familia.",
        "Recibiendo un premio por logros escolares.",
        "Ayudando a un compañero en un momento de necesidad."
    ])
    impact_level = random.randint(1, 10)  # Random impact level between 1 and 10
    duration = random.randint(5, 20)  # Random duration in minutes

    # Use the MemoryBuilder to create a new memory
    memory_builder = MemoryBuilder()
    memory = (memory_builder
              .set_description(memory_description)
              .set_impact_level(impact_level)
              .set_duration(duration)
              .build())
    
    return memory.description  # Or you can return the full memory object if needed
