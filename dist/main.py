# main.py
import numpy as np
import retos_optimizacion as reto 

from algoritmos import (
    BusquedaAleatoria, EscaladaColinas, RecocidoSimulado,
    EscaladaColinasReinicios, BusquedaLocalReiterada
)
from framework import FrameworkComparacion
from afinador import AfinadorParametros

def main() -> None:
    np.random.seed(1)
    
    funciones_a_optimizar = [
        reto.Funcion_1(), reto.Funcion_2(), reto.Funcion_3(), reto.Funcion_4()
    ]
    
    algoritmos_a_comparar = [
        BusquedaAleatoria(),
        EscaladaColinas(),
        RecocidoSimulado(),
        EscaladaColinasReinicios(paciencia=100),
        BusquedaLocalReiterada(paciencia=100)
    ]
    
    framework = FrameworkComparacion(
        funciones=funciones_a_optimizar,
        algoritmos=algoritmos_a_comparar,
        presupuesto_por_funcion=10000
    )
    
    # --- CONFIGURACIÓN DEL AFINADOR (GRID SEARCH) ---
    # Le damos 100 iteraciones por cada prueba
    afinador = AfinadorParametros(presupuesto_por_prueba=100)
    
    # Definimos qué probar. 
    # Cuidado: Muchas combinaciones multiplicadas por 100 gastarán todo tu presupuesto.
    diccionario_grids = {
        EscaladaColinas: {
            'tamano_paso': [0.1, 0.5, 1.0, 2.0]  # 4 combinaciones = 400 llamadas gastadas
        },
        RecocidoSimulado: {
            'temperatura_inicial': [10.0, 100.0],
            'tasa_enfriamiento': [0.90, 0.99],
            'tamano_paso': [0.1, 1.0] 
            # 2 * 2 * 2 = 8 combinaciones = 800 llamadas gastadas
        },
        BusquedaLocalReiterada: {
            'tamano_paso': [0.5, 1.0],
            'tamano_salto': [2.0, 5.0],
            'paciencia': [50, 100]
            # 2 * 2 * 2 = 8 combinaciones = 800 llamadas gastadas
        }
    }
    
    # Inyectamos el afinador al framework
    framework.configurar_afinador(afinador, diccionario_grids)
    
    print("Iniciando laboratorio de optimización heurística...")
    framework.ejecutar_experimento()
    framework.imprimir_resumen()

if __name__ == "__main__":
    main()