# base.py
import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Tuple, List

class AlgoritmoOptimizacion(ABC):
    """
    Clase base abstracta para algoritmos de optimización de trayectoria única.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.limite_inferior: float = -10.0
        self.limite_superior: float = 10.0
        
        # NUEVO LAB 8: Atributo para guardar la evolución del mejor valor encontrado.
        # Almacenará el mejor fitness en la evaluación 1, 2, 3... hasta el final.
        self.historial_convergencia: List[float] = []

    def generar_punto_aleatorio(self, dimensiones: int) -> np.ndarray:
        """Genera un punto aleatorio dentro del espacio de búsqueda permitido."""
        return np.random.uniform(
            low=self.limite_inferior, 
            high=self.limite_superior, 
            size=dimensiones
        )

    # NUEVO LAB 8: Método para limpiar la memoria antes de una nueva ejecución
    def reiniciar_historial(self) -> None:
        """Limpia el historial de convergencia para una nueva prueba."""
        self.historial_convergencia = []

    @abstractmethod
    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        """
        Ejecuta la optimización.
        Devuelve una tupla con la mejor solución (vector) y su valor.
        """
        pass