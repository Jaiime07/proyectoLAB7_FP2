# afinador.py
import itertools
from typing import Any, Dict, List, Type
from base import AlgoritmoOptimizacion

class AfinadorParametros:
    """
    Clase encargada de realizar una búsqueda en cuadrícula (Grid Search) para 
    encontrar los mejores hiperparámetros de un algoritmo dado, respetando un presupuesto.
    """
    
    def __init__(self, presupuesto_por_prueba: int) -> None:
        """
        Args:
            presupuesto_por_prueba (int): Número de evaluaciones que se gastarán 
                                          evaluando cada combinación de parámetros.
        """
        self.presupuesto_por_prueba: int = presupuesto_por_prueba


    def buscar_mejores_parametros(self, clase_algoritmo: Type[AlgoritmoOptimizacion], 
                                  funcion: Any, 
                                  grid_parametros: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Prueba diferentes combinaciones de parámetros ejecutando el algoritmo y 
        devuelve la configuración que obtuvo el menor valor.
        
        Args:
            clase_algoritmo (Type[AlgoritmoOptimizacion]): La clase del algoritmo (ej. EscaladaColinas).
            funcion (Any): Objeto de la función a optimizar.
            grid_parametros (Dict[str, List[Any]]): Diccionario con los nombres de los parámetros 
                                                    y las listas de valores a probar.
                                                    
        Returns:
            Dict[str, Any]: Diccionario con la mejor combinación de parámetros.
        """

        mejores_parametros: Dict[str, Any] = {}
        mejor_valor_global: float = float('inf')

        # Extraemos los nombres de los parámetros y sus posibles valores
        nombres_parametros: List[str] = list(grid_parametros.keys())
        valores_parametros: List[List[Any]] = list(grid_parametros.values())

        # itertools.product hace producto cartesiano
        for combinacion in itertools.product(*valores_parametros): # * para unpacking
            # Emparejamos los nombres con la combinación actual (ej. {'tamano_paso': 0.1})
            configuracion_actual: Dict[str, Any] = dict(zip(nombres_parametros, combinacion))
            
            # Instanciamos el algoritmo pasando los parámetros desempaquetados 
            algoritmo: AlgoritmoOptimizacion = clase_algoritmo(**configuracion_actual)
            
            # Ejecutamos el algoritmo para probar qué tan buena es esta configuración
            _, mejor_valor = algoritmo.ejecutar(
                funcion=funcion, 
                presupuesto=self.presupuesto_por_prueba
            )
            
            if mejor_valor < mejor_valor_global:
                mejor_valor_global = mejor_valor
                mejores_parametros = configuracion_actual
                
        return mejores_parametros