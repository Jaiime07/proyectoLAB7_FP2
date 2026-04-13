# framework.py
from typing import Any, List, Dict
from base import AlgoritmoOptimizacion

class FrameworkComparacion:
    """
    Orquesta la ejecución de los experimentos y recopila los resultados.
    """

    def __init__(self, funciones: List[Any], algoritmos: List[AlgoritmoOptimizacion], presupuesto_por_funcion: int = 10000) -> None:
        """
        Inicializa el framework.
        
        Args:
            funciones (List[Any]): Lista de funciones a optimizar.
            algoritmos (List[AlgoritmoOptimizacion]): Lista de algoritmos a usar.
            presupuesto_por_funcion (int): Evaluaciones máximas por función.
        """
        self.funciones: List[Any] = funciones
        self.algoritmos: List[AlgoritmoOptimizacion] = algoritmos
        self.presupuesto_por_funcion: int = presupuesto_por_funcion
        # Diccionario para guardar resultados: {Nombre_Funcion: {Nombre_Algoritmo: Mejor_Valor}}
        self.resultados: Dict[str, Dict[str, float]] = {}

    def ejecutar_experimento(self) -> None:
        """
        Itera sobre las funciones y algoritmos para buscar los mínimos.
        """
        for i, funcion in enumerate(self.funciones, start=1):
            nombre_funcion: str = f"Funcion_{i}"
            self.resultados[nombre_funcion] = {}
            print(f"\n--- Optimizando {nombre_funcion} ---")
            
            for algoritmo in self.algoritmos:
                # Reiniciamos el contador interno de la función proporcionada en el reto
                funcion.reiniciar_contador()
                
                # Ejecutamos el algoritmo
                _, mejor_valor = algoritmo.ejecutar(
                    funcion=funcion, 
                    presupuesto=self.presupuesto_por_funcion
                )
                
                # Guardamos el resultado
                self.resultados[nombre_funcion][algoritmo.nombre] = mejor_valor
                print(f"[{algoritmo.nombre}] Mejor valor encontrado: {mejor_valor:.4f}")

    def imprimir_resumen(self) -> None:
        """Muestra un resumen final de los resultados."""
        print("\n" + "="*40)
        print("RESUMEN FINAL DE OPTIMIZACIÓN")
        print("="*40)
        for nombre_func, resultados_algoritmos in self.resultados.items():
            print(f"\n{nombre_func}:")
            for nombre_alg, valor in resultados_algoritmos.items():
                print(f"  - {nombre_alg}: {valor:.6f}")