# algoritmos.py
import numpy as np
from typing import Any, Tuple
from base import AlgoritmoOptimizacion

class BusquedaAleatoria(AlgoritmoOptimizacion):
    """
    Implementa el algoritmo de Búsqueda Aleatoria (Random Search).
    Genera puntos al azar en el espacio de búsqueda y se queda con el mejor.
    """

    def __init__(self) -> None:
        """Inicializa el algoritmo con su nombre correspondiente."""
        super().__init__(nombre="Búsqueda Aleatoria")

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        """
        Ejecuta la búsqueda aleatoria.
        
        Args:
            funcion (Any): Función a minimizar.
            presupuesto (int): Número máximo de llamadas a evaluar.
            dimensiones (int): Dimensión del problema.
            
        Returns:
            Tuple[np.ndarray, float]: El mejor vector encontrado y su evaluación.
        """
        # 1. Generamos un primer punto inicial al azar y lo evaluamos
        mejor_solucion: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        mejor_valor: float = funcion.evaluar(mejor_solucion)
        evaluaciones_gastadas: int = 1
        
        # 2. Bucle principal hasta agotar el presupuesto
        while evaluaciones_gastadas < presupuesto:
            # Generamos un nuevo candidato
            candidato: np.ndarray = self.generar_punto_aleatorio(dimensiones)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            # Si el candidato es mejor (menor valor), actualizamos el mejor encontrado
            if valor_candidato < mejor_valor:
                mejor_solucion = candidato
                mejor_valor = valor_candidato
                
        return mejor_solucion, mejor_valor 
    

import math 

class EscaladaColinas(AlgoritmoOptimizacion):
    """
    Algoritmo de Escalada de Colinas (Hill Climbing).
    Genera un vecino cercano a la solución actual. Si es mejor, se mueve a él.
    """

    def __init__(self, tamano_paso: float = 0.5) -> None:
        """
        Inicializa el algoritmo.
        
        Args:
            tamano_paso (float): Qué tan grande será la perturbación para generar un vecino.
        """
        super().__init__(nombre=f"Escalada de Colinas (paso={tamano_paso})")
        self.tamano_paso: float = tamano_paso

    def generar_vecino(self, solucion_actual: np.ndarray) -> np.ndarray:
        """
        Genera una nueva solución sumando un pequeño ruido aleatorio a la actual.
        Asegura que el vecino se mantenga dentro de los límites [-10, 10].
        """
        ruido = np.random.uniform(-self.tamano_paso, self.tamano_paso, size=solucion_actual.shape)
        vecino = solucion_actual + ruido
        # np.clip "recorta" los valores para que no se salgan de los límites
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        solucion_actual: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        valor_actual: float = funcion.evaluar(solucion_actual)
        evaluaciones_gastadas: int = 1
        
        while evaluaciones_gastadas < presupuesto:
            candidato: np.ndarray = self.generar_vecino(solucion_actual)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            # Solo nos movemos si el vecino es estrictamente mejor (menor valor)
            if valor_candidato < valor_actual:
                solucion_actual = candidato
                valor_actual = valor_candidato
                
        return solucion_actual, valor_actual


class RecocidoSimulado(AlgoritmoOptimizacion):
    """
    Algoritmo de Recocido Simulado (Simulated Annealing).
    Permite movimientos a peores soluciones para escapar de mínimos locales.
    """

    def __init__(self, temperatura_inicial: float = 100.0, tasa_enfriamiento: float = 0.99, tamano_paso: float = 0.5) -> None:
        """
        Inicializa el algoritmo.
        
        Args:
            temperatura_inicial (float): Temperatura de inicio (probabilidad de aceptar peores soluciones).
            tasa_enfriamiento (float): Multiplicador para reducir la temperatura en cada iteración.
            tamano_paso (float): Magnitud de la perturbación para generar vecinos.
        """
        super().__init__(nombre=f"Recocido Simulado (T0={temperatura_inicial}, alfa={tasa_enfriamiento})")
        self.temperatura_inicial: float = temperatura_inicial
        self.tasa_enfriamiento: float = tasa_enfriamiento
        self.tamano_paso: float = tamano_paso

    def generar_vecino(self, solucion_actual: np.ndarray) -> np.ndarray:
        ruido = np.random.uniform(-self.tamano_paso, self.tamano_paso, size=solucion_actual.shape)
        vecino = solucion_actual + ruido
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        solucion_actual: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        valor_actual: float = funcion.evaluar(solucion_actual)
        evaluaciones_gastadas: int = 1
        
        mejor_solucion_global: np.ndarray = solucion_actual.copy()
        mejor_valor_global: float = valor_actual
        temperatura: float = self.temperatura_inicial
        
        while evaluaciones_gastadas < presupuesto:
            candidato: np.ndarray = self.generar_vecino(solucion_actual)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            diferencia: float = valor_candidato - valor_actual
            
            # Si es mejor (diferencia negativa) o si cumple la probabilidad, aceptamos
            if diferencia < 0 or np.random.rand() < math.exp(-diferencia / temperatura):  # .exp() es e^(-diferencia/temperatura)
                solucion_actual = candidato
                valor_actual = valor_candidato
                
                # Actualizamos el mejor global encontrado en toda la historia
                if valor_actual < mejor_valor_global:
                    mejor_solucion_global = solucion_actual.copy()
                    mejor_valor_global = valor_actual
            
            # Enfriamos el sistema
            temperatura *= self.tasa_enfriamiento
            # Evitamos división por cero por errores de precisión de punto flotante
            temperatura = max(temperatura, 1e-10) 
                
        return mejor_solucion_global, mejor_valor_global