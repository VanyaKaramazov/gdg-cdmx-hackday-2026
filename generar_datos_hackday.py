import pandas as pd
import random
from datetime import datetime, timedelta

def generar_datos_clinica():
    # Inventario de clínica
    medicamentos = ['Paracetamol', 'Metformina', 'Captopril', 'Insulina', 'Amoxicilina']
    inv = [[m, random.randint(2, 50), random.choice(['Urgente', 'Normal'])] for m in medicamentos]
    pd.DataFrame(inv, columns=['Medicamento', 'Stock', 'Prioridad']).to_csv('clinica_inventario.csv', index=False)
    
    # Flujo de pacientes
    pacientes = [[f"Paciente_{i}", random.randint(5, 80), random.choice(['Fiebre', 'Hipertensión', 'Infección'])] for i in range(1, 21)]
    pd.DataFrame(pacientes, columns=['ID', 'Edad', 'Sintoma_Principal']).to_csv('clinica_pacientes.csv', index=False)
    print("✅ Datos de Clínica generados.")


# Ejecutar las tres funciones para tener todo listo
#generar_datos_clinica()