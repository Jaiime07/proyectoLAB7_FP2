# base.py
import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Tuple

class AlgoritmoOptimizacion(ABC):
    """
    Clase base abstracta para algoritmos de optimización de trayectoria única.
    
    Attributes:
        nombre (str): El nombre descriptivo del algoritmo.
        limite_inferior (float): Límite inferior del espacio de búsqueda.
        limite_superior (float): Límite superior del espacio de búsqueda.
    """

    def __init__(self, nombre: str) -> None:
        """
        Inicializa la clase base del algoritmo.
        
        Args:
            nombre (str): Nombre del algoritmo (ej. 'Búsqueda Aleatoria').
        """
        self.nombre: str = nombre
        self.limite_inferior: float = -10.0
        self.limite_superior: float = 10.0

    def generar_punto_aleatorio(self, dimensiones: int) -> np.ndarray:
        """
        Genera un punto aleatorio dentro del espacio de búsqueda permitido.
        
        Args:
            dimensiones (int): Número de dimensiones del vector.
            
        Returns:
            np.ndarray: Array de numpy con valores aleatorios.
        """
        return np.random.uniform(
            low=self.limite_inferior, 
            high=self.limite_superior, 
            size=dimensiones
        )

    @abstractmethod
    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        """
        Ejecuta la optimización. Debe ser implementado por las clases hijas.
        
        Args:
            funcion (Any): Objeto de la función a optimizar.
            presupuesto (int): Límite de evaluaciones permitidas.
            dimensiones (int): Dimensión del problema (por defecto 10).
            
        Returns:
            Tuple[np.ndarray, float]: Tupla con la mejor solución (vector) y su valor.
        """
        pass