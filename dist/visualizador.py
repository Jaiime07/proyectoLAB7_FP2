# visualizador.py
import matplotlib.pyplot as plt
from typing import List

# NUEVO LAB 8: Clase dedicada a la visualización de datos (Single Responsibility Principle)
class VisualizadorConvergencia:
    """
    Clase encargada de renderizar las gráficas de evolución de los algoritmos.
    """

    @staticmethod
    def graficar_curva(historial: List[float], titulo: str = "Curva de Convergencia") -> None:
        """
        Genera y muestra una gráfica de la curva de convergencia.
        
        Args:
            historial (List[float]): Lista con los mejores valores encontrados en cada iteración.
            titulo (str): Título principal de la gráfica.
        """
        # Verificamos que haya datos para evitar errores
        if not historial:
            print("[Visualizador] No hay datos en el historial para graficar.")
            return

        # NUEVO LAB 8: Configuración de la figura y los ejes usando matplotlib
        plt.figure(figsize=(10, 6))
        
        # Generamos el eje X (Número de evaluaciones, de 1 hasta la longitud del historial)
        eje_x = list(range(1, len(historial) + 1))
        
        # Dibujamos la línea azul oscura solicitada en el PDF
        plt.plot(eje_x, historial, color='darkblue', label='Mejor Fitness')

        # Configuramos la escala logarítmica para el eje Y tal como pide el PDF
        plt.yscale('log')
        
        # Añadimos cuadrícula para facilitar la lectura
        plt.grid(True, which="both", ls="--", alpha=0.5)
        
        # Títulos y etiquetas
        plt.title(titulo, fontsize=14)
        plt.xlabel('Número de Evaluaciones', fontsize=12)
        plt.ylabel('Valor de la Función (Fitness)', fontsize=12)
        plt.legend()
        
        # Mostramos la ventana con la gráfica
        plt.show()