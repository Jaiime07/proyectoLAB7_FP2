# framework.py
from typing import Any, List, Dict, Type
from base import AlgoritmoOptimizacion
from afinador import AfinadorParametros

class FrameworkComparacion:
    """
    Orquesta la ejecución de los experimentos, integra el afinado de parámetros
    y recopila los resultados respetando el presupuesto global.
    """

    def __init__(self, funciones: List[Any], algoritmos: List[AlgoritmoOptimizacion], presupuesto_por_funcion: int = 10000) -> None:
        self.funciones: List[Any] = funciones
        self.algoritmos_instanciados: List[AlgoritmoOptimizacion] = algoritmos
        self.presupuesto_por_funcion: int = presupuesto_por_funcion
        self.resultados: Dict[str, Dict[str, float]] = {}
        
        # Configuración opcional para el Grid Search
        self.afinador: AfinadorParametros | None = None
        self.grids_parametros: Dict[str, Dict[str, List[Any]]] = {}
        self.clases_a_afinar: Dict[str, Type[AlgoritmoOptimizacion]] = {}

    def configurar_afinador(self, afinador: AfinadorParametros, config_afinado: Dict[Type[AlgoritmoOptimizacion], Dict[str, List[Any]]]) -> None:
        """
        Configura qué algoritmos serán afinados y con qué hiperparámetros.
        """
        self.afinador = afinador
        # Guardamos usando el nombre de la clase como clave para buscarlo fácilmente
        self.grids_parametros = {cls.__name__: grid for cls, grid in config_afinado.items()}
        self.clases_a_afinar = {cls.__name__: cls for cls in config_afinado.keys()}

    def ejecutar_experimento(self) -> None:
        for i, funcion in enumerate(self.funciones, start=1):
            nombre_funcion: str = f"Funcion_{i}"
            self.resultados[nombre_funcion] = {}
            print(f"\n--- Optimizando {nombre_funcion} ---")
            
            for algoritmo_base in self.algoritmos_instanciados:
                # 1. Reiniciamos a 0 las invocaciones en la función
                funcion.reiniciar_contador()
                presupuesto_restante: int = self.presupuesto_por_funcion
                
                nombre_clase: str = algoritmo_base.__class__.__name__
                algoritmo_final: AlgoritmoOptimizacion = algoritmo_base
                
                # 2. Fase de Afinado (Grid Search) si la clase está configurada
                if self.afinador is not None and nombre_clase in self.grids_parametros:
                    print(f"  [Afinando] {algoritmo_base.nombre}...")
                    grid = self.grids_parametros[nombre_clase]
                    clase_alg = self.clases_a_afinar[nombre_clase]
                    
                    # Ejecutamos las pruebas (esto suma invocaciones al contador de la función)
                    mejores_params = self.afinador.buscar_mejores_parametros(
                        clase_algoritmo=clase_alg,
                        funcion=funcion,
                        grid_parametros=grid
                    )
                    
                    # Descontamos exactamente lo que el afinador gastó usando la propiedad del profesor
                    presupuesto_restante -= funcion.presupuesto_gastado
                    
                    # Instanciamos el algoritmo definitivo con los parámetros ganadores
                    algoritmo_final = clase_alg(**mejores_params)
                    print(f"  -> Mejores params: {mejores_params} (Presupuesto restante: {presupuesto_restante})")
                    
                # 3. Fase de Ejecución Final
                _, mejor_valor = algoritmo_final.ejecutar(
                    funcion=funcion, 
                    presupuesto=presupuesto_restante
                )
                
                self.resultados[nombre_funcion][algoritmo_final.nombre] = mejor_valor
                print(f"[{algoritmo_final.nombre}] Mejor valor final: {mejor_valor:.4f}")

    def imprimir_resumen(self) -> None:
        print("\n" + "="*50)
        print("RESUMEN FINAL DE OPTIMIZACIÓN (INCLUYENDO AFINADO)")
        print("="*50)
        for nombre_func, resultados_algoritmos in self.resultados.items():
            print(f"\n{nombre_func}:")
            for nombre_alg, valor in resultados_algoritmos.items():
                print(f"  - {nombre_alg}: {valor:.6f}")