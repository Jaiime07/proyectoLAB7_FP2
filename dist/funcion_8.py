# funcion_8.py
import numpy as np
import retos_optimizacion as reto

# NUEVO LAB 8: Implementación explícita de la Función de Schwefel modificada
class Funcion_8_modificada(reto._BaseOpt):
    """
    Función de Schwefel trasladada para que el mínimo (0.0) se alcance 
    en el vector x = [1.0, 1.0, ..., 1.0].
    Límites de búsqueda recomendados: [-500, 500].
    """
    def __init__(self) -> None:
        # Desplazamiento proporcionado en el PDF para mover el mínimo a [1.0]*10
        shift_vectors = [-419.9687] * 10
        super().__init__(shift_vectors)

    def evaluar(self, x: np.ndarray) -> float:
        """Evalúa la función matemática de Schwefel."""
        z = self._preparar_x(x)
        z = z - self._shift
        
        # Evaluamos la sumatoria de z * sen(sqrt(|z|))
        sum_term = np.sum(z * np.sin(np.sqrt(np.abs(z))))
        
        # Retorno de la fórmula matemática ajustada a 0
        return float(418.9828872724338 * self._dims - sum_term)