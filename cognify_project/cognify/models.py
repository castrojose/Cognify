from django.db import models
from django.utils import timezone

class CrimeType(models.TextChoices):
    VIOLENT = 'Violent', 'Violent'
    FINANCIAL = 'Financial', 'Financial'
    HATE = 'Hate', 'Hate'

class Criminal(models.Model):
    name = models.CharField(max_length=100)
    crime_type = models.CharField(max_length=50)
    implanted_memories = models.TextField(blank=True, null=True)
    rehabilitation_status = models.CharField(
        max_length=50,
        choices=[('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='in_progress'
    )
    rehabilitation_success_percentage = models.FloatField(default=0.0)  # Correct field
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Memory(models.Model):
    criminal = models.ForeignKey(Criminal, related_name='memories', on_delete=models.CASCADE)
    description = models.TextField()
    impact_level = models.IntegerField()  # Nivel de impacto emocional
    duration = models.PositiveIntegerField()  # Duración percibida en minutos

    def __str__(self):
        return f"Memory for {self.criminal.name} (Impact: {self.impact_level})"

class Simulation(models.Model):
    criminal = models.ForeignKey(Criminal, related_name='simulations', on_delete=models.CASCADE)
    date_run = models.DateTimeField(default=timezone.now)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Simulation for {self.criminal.name} on {self.date_run}"
