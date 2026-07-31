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

def generar_datos_negocio():
    # Ventas diarias
    ventas = [[f"2026-07-{31-i}", random.randint(500, 3000), random.randint(200, 1500)] for i in range(10)]
    pd.DataFrame(ventas, columns=['Fecha', 'Ingresos', 'Egresos']).to_csv('negocio_flujo.csv', index=False)
    
    # Mercado local
    mercado = [['Harina', 25.50], ['Azúcar', 30.00], ['Huevo', 45.00]]
    pd.DataFrame(mercado, columns=['Insumo', 'Precio_Promedio']).to_csv('negocio_mercado.csv', index=False)
    print("✅ Datos de Negocio generados.")

def generar_datos_escuela():
    # Calificaciones
    alumnos = [[f"Alumno_{i}", random.randint(5, 10), random.choice(['Álgebra', 'Fracciones', 'Geometría'])] for i in range(1, 16)]
    pd.DataFrame(alumnos, columns=['ID_Alumno', 'Calificacion', 'Tema_Fallo']).to_csv('escuela_rendimiento.csv', index=False)
    print("✅ Datos de Escuela generados.")

# Ejecutar las tres funciones para tener todo listo
generar_datos_clinica()
generar_datos_negocio()
generar_datos_escuela()