# framework.py
import numpy as np
from typing import Any, List, Dict, Type, Tuple
from base import AlgoritmoOptimizacion
from afinador import AfinadorParametros

class FrameworkComparacion:
    """
    Orquesta la ejecución de los experimentos, integra el afinado de parámetros
    y recopila los resultados (incluyendo el vector solución) respetando el presupuesto.
    """

    def __init__(self, funciones: List[Any], algoritmos: List[AlgoritmoOptimizacion], presupuesto_por_funcion: int = 10000) -> None:
        self.funciones: List[Any] = funciones
        self.algoritmos_instanciados: List[AlgoritmoOptimizacion] = algoritmos
        self.presupuesto_por_funcion: int = presupuesto_por_funcion
        
        # ACTULIZACIÓN: Ahora el diccionario guarda una Tupla con el vector (np.ndarray) y el valor (float)
        self.resultados: Dict[str, Dict[str, Tuple[np.ndarray, float]]] = {}
        
        # Configuración opcional para el Grid Search
        self.afinador: AfinadorParametros | None = None
        self.grids_parametros: Dict[str, Dict[str, List[Any]]] = {}
        self.clases_a_afinar: Dict[str, Type[AlgoritmoOptimizacion]] = {}

    def configurar_afinador(self, afinador: AfinadorParametros, config_afinado: Dict[Type[AlgoritmoOptimizacion], Dict[str, List[Any]]]) -> None:
        """Configura qué algoritmos serán afinados y con qué hiperparámetros."""
        self.afinador = afinador
        self.grids_parametros = {cls.__name__: grid for cls, grid in config_afinado.items()}
        self.clases_a_afinar = {cls.__name__: cls for cls in config_afinado.keys()}

    def ejecutar_experimento(self) -> None:
        for i, funcion in enumerate(self.funciones, start=1):
            nombre_funcion: str = f"Funcion_{i}"
            self.resultados[nombre_funcion] = {}
            print(f"\n--- Optimizando {nombre_funcion} ---")
            
            for algoritmo_base in self.algoritmos_instanciados:
                funcion.reiniciar_contador()
                presupuesto_restante: int = self.presupuesto_por_funcion
                
                nombre_clase: str = algoritmo_base.__class__.__name__
                algoritmo_final: AlgoritmoOptimizacion = algoritmo_base
                
                # Fase de Afinado (Grid Search)
                if self.afinador is not None and nombre_clase in self.grids_parametros:
                    print(f"  [Afinando] {algoritmo_base.nombre}...")
                    grid = self.grids_parametros[nombre_clase]
                    clase_alg = self.clases_a_afinar[nombre_clase]
                    
                    mejores_params = self.afinador.buscar_mejores_parametros(
                        clase_algoritmo=clase_alg,
                        funcion=funcion,
                        grid_parametros=grid
                    )
                    
                    presupuesto_restante -= funcion.presupuesto_gastado
                    algoritmo_final = clase_alg(**mejores_params)
                    print(f"  -> Mejores params: {mejores_params} (Presupuesto restante: {presupuesto_restante})")
                    
                # Fase de Ejecución Final
                # ACTUALIZACIÓN: Ahora sí recogemos 'mejor_vector' en lugar de usar '_'
                mejor_vector, mejor_valor = algoritmo_final.ejecutar(
                    funcion=funcion, 
                    presupuesto=presupuesto_restante
                )
                
                # Guardamos ambos datos en nuestro diccionario de resultados
                self.resultados[nombre_funcion][algoritmo_final.nombre] = (mejor_vector, mejor_valor)
                print(f"[{algoritmo_final.nombre}] Mejor valor final: {mejor_valor:.4f}")

    def imprimir_resumen(self) -> None:
        """Imprime el resumen final formateando los vectores para que sean legibles."""
        print("\n" + "="*80)
        print("RESUMEN FINAL DE OPTIMIZACIÓN (INCLUYENDO VECTORES)")
        print("="*80)
        
        for nombre_func, resultados_algoritmos in self.resultados.items():
            print(f"\n{nombre_func}:")
            for nombre_alg, (vector, valor) in resultados_algoritmos.items():
                
                # Usamos np.array2string para dar un formato limpio al vector de 10 dimensiones
                # precision=4: Muestra 4 decimales
                # suppress_small=True: Convierte números extremadamente cercanos a 0 (ej. 1e-16) en 0.0
                vector_formateado = np.array2string(vector, precision=4, suppress_small=True, separator=', ')
                
                print(f"  - {nombre_alg}:")
                print(f"      Valor (f(x)): {valor:.6f}")
                print(f"      Vector (x)  : {vector_formateado}")