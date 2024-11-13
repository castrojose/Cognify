from django.shortcuts import render, get_object_or_404, redirect
from .models import Criminal, Simulation, Memory
from django.http import HttpResponse
from .models import CrimeType
from .utils import SimulationConfig, MemoryBuilder
from .forms import CriminalForm


def criminal_list(request):
    criminals = Criminal.objects.all()
    return render(request, 'cognify/criminal_list.html', {'criminals': criminals})

def run_simulation(request, criminal_id):
    criminal = get_object_or_404(Criminal, id=criminal_id)
    simulation = Simulation.objects.create(criminal=criminal, successful=True)
    criminal.rehabilitated = True
    criminal.save()
    return redirect('criminal_list')

def impact_evaluation(request):
    total_simulations = Simulation.objects.count()
    successful_simulations = Simulation.objects.filter(successful=True).count()
    return render(request, 'cognify/impact_evaluation.html', {
        'total_simulations': total_simulations,
        'successful_simulations': successful_simulations,
    })



def create_custom_memory(criminal):
    builder = MemoryBuilder()
    if criminal.crime_type == CrimeType.VIOLENT:
        memory = (
            builder
            .set_description("Empathy for victim's suffering")
            .set_impact_level(5)
            .set_duration(60)
            .build()
        )
    elif criminal.crime_type == CrimeType.FINANCIAL:
        memory = (
            builder
            .set_description("Understanding financial damage")
            .set_impact_level(3)
            .set_duration(45)
            .build()
        )
    # Guarda el recuerdo en la base de datos
    memory.criminal = criminal
    memory.save()
    return memory

def run_simulation(request, criminal_id):
    criminal = get_object_or_404(Criminal, id=criminal_id)
    config = SimulationConfig()
    config.config['simulate'] = True  # Ejemplo de uso de Singleton

    # Crear un recuerdo personalizado
    create_custom_memory(criminal)

    simulation = Simulation.objects.create(criminal=criminal, successful=True)
    criminal.rehabilitated = True
    criminal.save()
    return redirect('criminal_list')

# cognify/views.py


def add_criminal(request):
    if request.method == "POST":
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criminal_list')
    else:
        form = CriminalForm()
    return render(request, 'cognify/add_criminal.html', {'form': form})

from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Cargar el modelo y el tokenizador preentrenados
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def generate_memory(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
    memory = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return memory



# En views.py
import random

def rehabilitate_criminal_with_ai(criminal_id):
    criminal = Criminal.objects.get(id=criminal_id)
    
    # Generar un recuerdo positivo usando IA
    prompt = "Recuerdo positivo de la infancia."
    new_memory = generate_memory(prompt)  # Función que ya creaste para generar recuerdos
    
    # Asignar el recuerdo al criminal
    criminal.implanted_memories = new_memory

    # Calcular el porcentaje de rehabilitación (esto es un ejemplo básico, puedes hacer que sea más complejo)
    # Podrías usar un modelo predictivo para generar este porcentaje basado en más variables
    rehabilitation_percentage = random.uniform(60.0, 90.0)  # Porcentaje aleatorio entre 60 y 90
    criminal.rehabilitation_success_percentage = rehabilitation_percentage
    
    # Marcar como rehabilitado si el porcentaje es alto
    if rehabilitation_percentage > 75:
        criminal.rehabilitation_status = "completed"
    
    criminal.save()
    return criminal
