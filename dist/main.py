# main.py
import numpy as np
import retos_optimizacion2 as reto 

# Importamos todos los algoritmos desarrollados
from algoritmos import (
    BusquedaAleatoria, 
    EscaladaColinas, 
    RecocidoSimulado,
    EscaladaColinasReinicios, 
    BusquedaLocalReiterada,
    EscaladaColinasDinamica # NUEVO LAB 8
)
from funcion_8 import Funcion_8_modificada # NUEVO LAB 8
from framework import FrameworkComparacion
from afinador import AfinadorParametros

def main() -> None:
    # 1. Fijar semilla para reproducibilidad [cite: 179]
    np.random.seed(1)
    
    # 2. Definir TODAS las funciones a evaluar [cite: 113, 114]
    # Nota: Asegúrate de que tu archivo 'retos_optimizacion.py' contenga las funciones 5, 6 y 7.
    funciones_a_optimizar = [
        reto.Funcion_1(), reto.Funcion_2(), reto.Funcion_3(), reto.Funcion_4(),
        reto.Funcion_5(), reto.Funcion_6(), reto.Funcion_7(),
        Funcion_8_modificada() # La función de Schwefel del Lab 8 [cite: 138]
    ]
    
    # 3. Definir TODOS los algoritmos a comparar
    algoritmos_a_comparar = [
        BusquedaAleatoria(),
        EscaladaColinas(tamano_paso=0.5),
        RecocidoSimulado(temperatura_inicial=100.0, tasa_enfriamiento=0.99),
        EscaladaColinasReinicios(paciencia=100),
        BusquedaLocalReiterada(paciencia=100),
        EscaladaColinasDinamica(paso_inicial=2.0, paso_final=0.01) # Algoritmo dinámico [cite: 115]
    ]
    
    # 4. Configurar el presupuesto (40.000 evaluaciones como sugiere el Lab 8) 
    presupuesto_por_func = 40000
    
    framework = FrameworkComparacion(
        funciones=funciones_a_optimizar,
        algoritmos=algoritmos_a_comparar,
        presupuesto_por_funcion=presupuesto_por_func
    )
    
    # 5. Opcional: Configurar afinador para los algoritmos que lo requieran
    # (Si quieres ir rápido, puedes omitir este paso comentando las líneas del afinador)
    afinador = AfinadorParametros(presupuesto_por_prueba=200)
    config_grids = {
        EscaladaColinasDinamica: {
            'paso_inicial': [2.0, 5.0, 10.0],
            'paso_final': [0.01, 0.001]
        }
    }
    framework.configurar_afinador(afinador, config_grids)
    
    # 6. Ejecución del experimento completo
    print(f"Iniciando experimento global: {len(funciones_a_optimizar)} funciones x {len(algoritmos_a_comparar)} algoritmos.")
    print(f"Presupuesto total por función: {presupuesto_por_func} evaluaciones.")
    
    # Esto mostrará en pantalla el progreso de CADA par (Función, Algoritmo)
    framework.ejecutar_experimento()
    
    # 7. Mostrar el resumen final y exportar a CSV
    framework.imprimir_resumen()
    framework.exportar_csv("comparativa_completa_lab8.csv")

if __name__ == "__main__":
    main()