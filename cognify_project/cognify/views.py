from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Criminal, Simulation, Memory, CrimeType
from .utils import SimulationConfig, MemoryBuilder
from .forms import CriminalForm
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
# cognify/views.py
from .utils import generate_memory
import random
from django.shortcuts import get_object_or_404

# Load the GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# List of criminals
def criminal_list(request):
    criminals = Criminal.objects.all()
    return render(request, 'cognify/criminal_list.html', {'criminals': criminals})

# Function to run the simulation and create a custom memory
def run_simulation(request, criminal_id):
    criminal = get_object_or_404(Criminal, id=criminal_id)

    # Create configuration for the simulation
    config = SimulationConfig()
    config.config['simulate'] = True  # Example configuration using Singleton

    # Create a custom memory for the criminal
    create_custom_memory(criminal)

    # Register the simulation as successful
    Simulation.objects.create(criminal=criminal, successful=True)

    # Update the rehabilitation status of the criminal
    criminal.rehabilitated = True
    criminal.save()

    # Success message
    messages.success(request, f"La simulación para {criminal.name} fue exitosa.")

    return redirect('criminal_list')

# Impact evaluation function
def impact_evaluation(request):
    total_simulations = Simulation.objects.count()
    successful_simulations = Simulation.objects.filter(successful=True).count()
    return render(request, 'cognify/impact_evaluation.html', {
        'total_simulations': total_simulations,
        'successful_simulations': successful_simulations,
    })

# Create a custom memory based on the type of crime of the criminal
def create_custom_memory(criminal):
    builder = MemoryBuilder()

    # Determine the type of memory to create based on the crime type
    if criminal.crime_type == CrimeType.VIOLENT:
        memory = (
            builder
            .set_description("Empathy for victim's suffering")
            .set_impact_level(5)  # Ensure impact_level is set here
            .set_duration(60)
            .build()
        )
    elif criminal.crime_type == CrimeType.FINANCIAL:
        memory = (
            builder
            .set_description("Understanding financial damage")
            .set_impact_level(3)  # Ensure impact_level is set here
            .set_duration(45)
            .build()
        )
    else:
        # Provide a default impact level in case of an unexpected crime type
        memory = (
            builder
            .set_description("General awareness of wrongdoing")
            .set_impact_level(2)
            .set_duration(30)
            .build()
        )

    # Associate the memory with the criminal and save it to the database
    memory.criminal = criminal
    memory.save()
    return memory


# Add a new criminal
def add_criminal(request):
    if request.method == "POST":
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Criminal agregado exitosamente.")
            return redirect('criminal_list')
    else:
        form = CriminalForm()
    return render(request, 'cognify/add_criminal.html', {'form': form})

# Generate a positive memory using AI
def generate_ai_memory(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
    memory = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return memory

# Rehabilitate a criminal with AI
def rehabilitate_criminal_with_ai(criminal_id):
    criminal = get_object_or_404(Criminal, id=criminal_id)

    # Generate a positive memory using AI
    prompt = "Recuerdo positivo de la infancia."
    new_memory = generate_memory(prompt)

    # Assign the memory to the criminal
    criminal.implanted_memories = new_memory

    # Calculate a random success percentage for rehabilitation
    rehabilitation_percentage = random.uniform(60.0, 90.0)
    criminal.rehabilitation_success_percentage = rehabilitation_percentage

    # Update the rehabilitation status
    if rehabilitation_percentage > 75:
        criminal.rehabilitation_status = "completed"

    criminal.save()
    return criminal

def rehabilitate_criminal_with_progress(request, criminal_id):
    criminal = get_object_or_404(Criminal, id=criminal_id)

    # Generar un recuerdo positivo usando IA
    prompt = "Recuerdo positivo de la infancia."
    new_memory = generate_memory(prompt)
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Obtén el paso actual del progreso (con valor predeterminado de 0)
        current_step = int(request.GET.get('step', 0))
        
        # Definir los pasos del progreso
        progress_steps = [
            {"status": "Espere, estamos incrustando un recuerdo positivo...", "progress": 20},
            {"status": "Cargando... 50%", "progress": 50},
            {"status": "Cargando... 90%", "progress": 90},
            {"status": "Recuerdo incrustado, verificando resultado...", "progress": 100},
        ]
        
        # Si el paso actual es menor que el número de pasos, devuelve el siguiente paso
        if current_step < len(progress_steps):
            step = progress_steps[current_step]
            return JsonResponse({
                "progress": step["progress"],
                "status": step["status"],
                "next_step": current_step + 1  # Devuelve el siguiente paso para la siguiente petición
            })
        
        # Último paso: asignar memoria y calcular el porcentaje de éxito
        criminal.implanted_memories = new_memory
        rehabilitation_percentage = random.uniform(60.0, 90.0)
        criminal.rehabilitation_success_percentage = rehabilitation_percentage
        criminal.rehabilitation_status = "completed" if rehabilitation_percentage > 75 else "incomplete"
        criminal.save()

        return JsonResponse({
            "progress": 100,
            "status": "Criminal rehabilitado exitosamente",
            "memory": new_memory
        })

    # Renderizar la página de rehabilitación
    return render(request, 'cognify/rehabilitate_criminal_with_progress.html', {'criminal': criminal})

