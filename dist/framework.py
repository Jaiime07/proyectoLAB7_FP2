# framework.py
import csv
import numpy as np
from typing import Any, List, Dict, Type, Tuple
from base import AlgoritmoOptimizacion
from afinador import AfinadorParametros

class FrameworkComparacion:
    """
    Orquesta la ejecución de los experimentos, integra el afinado de parámetros
    y recopila los resultados (incluyendo vectores) respetando el presupuesto.
    """

    def __init__(self, funciones: List[Any], algoritmos: List[AlgoritmoOptimizacion], presupuesto_por_funcion: int = 10000) -> None:
        self.funciones: List[Any] = funciones
        self.algoritmos_instanciados: List[AlgoritmoOptimizacion] = algoritmos
        self.presupuesto_por_funcion: int = presupuesto_por_funcion
        
        # Guardamos el vector (np.ndarray) y el valor (float)
        self.resultados: Dict[str, Dict[str, Tuple[np.ndarray, float]]] = {}
        
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
            # Extraemos el nombre real de la clase (ej. Funcion_5 o Funcion_8_modificada)
            nombre_funcion: str = funcion.__class__.__name__
            self.resultados[nombre_funcion] = {}
            print(f"\n--- Optimizando {nombre_funcion} ---")
            
            for algoritmo_base in self.algoritmos_instanciados:
                funcion.reiniciar_contador()
                
                # Limpiamos el historial del algoritmo antes de evaluar
                if hasattr(algoritmo_base, 'reiniciar_historial'):
                    algoritmo_base.reiniciar_historial()
                    
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
                    
                    if hasattr(algoritmo_final, 'reiniciar_historial'):
                        algoritmo_final.reiniciar_historial()
                        
                    print(f"  -> Mejores params: {mejores_params} (Presupuesto restante: {presupuesto_restante})")
                    
                # Fase de Ejecución Final
                mejor_vector, mejor_valor = algoritmo_final.ejecutar(
                    funcion=funcion, 
                    presupuesto=presupuesto_restante
                )
                
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
                vector_formateado = np.array2string(vector, precision=4, suppress_small=True, separator=', ')
                print(f"  - {nombre_alg}:")
                print(f"      Valor (f(x)): {valor:.6f}")
                print(f"      Vector (x)  : {vector_formateado}")

    def exportar_csv(self, nombre_archivo: str = "resultados_optimizacion.csv") -> None:
        """
        Exporta los resultados almacenados a un archivo CSV.
        """
        encabezados: List[str] = ["Funcion", "Algoritmo", "Valor_Minimo", "Vector_Coordenadas"]
        
        try:
            with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(encabezados)
                
                for nombre_func, dict_algs in self.resultados.items():
                    for nombre_alg, (vector, valor) in dict_algs.items():
                        vector_str: str = np.array2string(vector, separator=';').replace('\n', '')
                        escritor.writerow([nombre_func, nombre_alg, f"{valor:.8f}", vector_str])
            
            print(f"\n[Éxito] Resultados exportados correctamente a: {nombre_archivo}")
            
        except IOError as e:
            print(f"\n[Error] No se pudo escribir el archivo: {e}")