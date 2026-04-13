# main.py (Fragmento modificado)
from algoritmos import BusquedaAleatoria, EscaladaColinas, RecocidoSimulado
from framework import FrameworkComparacion
import retos_optimizacion as reto
import numpy as np

def main() -> None:
    np.random.seed(1)
    
    funciones_a_optimizar = [
        reto.Funcion_1(), reto.Funcion_2(),
        reto.Funcion_3(), reto.Funcion_4()
    ]
    
    # Aquí añadimos los nuevos competidores
    algoritmos_a_comparar = [
        BusquedaAleatoria(),
        EscaladaColinas(tamano_paso=0.5),
        RecocidoSimulado(temperatura_inicial=100.0, tasa_enfriamiento=0.99, tamano_paso=0.5)
    ]
    
    framework = FrameworkComparacion(
        funciones=funciones_a_optimizar,
        algoritmos=algoritmos_a_comparar,
        presupuesto_por_funcion=10000
    )
    
    print("Iniciando laboratorio de optimización heurística...")
    framework.ejecutar_experimento()
    framework.imprimir_resumen()

if __name__ == "__main__":
    main()