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
        Args:
            funcion (Any): Función a minimizar.
            presupuesto (int): Número máximo de llamadas a evaluar.
            dimensiones (int): Dimensión del problema.
            
        Returns:
            Tuple[np.ndarray, float]: El mejor vector encontrado y su evaluación.
        """
        # Punto inicial al azar
        mejor_solucion: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        mejor_valor: float = funcion.evaluar(mejor_solucion)
        evaluaciones_gastadas: int = 1
        
        while evaluaciones_gastadas < presupuesto:
            # Nuevo candidato
            candidato: np.ndarray = self.generar_punto_aleatorio(dimensiones)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            if valor_candidato < mejor_valor:
                mejor_solucion = candidato
                mejor_valor = valor_candidato
                
        return mejor_solucion, mejor_valor 
    

import math 

class EscaladaColinas(AlgoritmoOptimizacion):
    """
    Genera un vecino cercano a la solución actual. Si es mejor, se mueve a él.
    """

    def __init__(self, tamano_paso: float = 0.5) -> None:
        """
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
        # np.clip "recorta" los valores 
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:

        solucion_actual: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        valor_actual: float = funcion.evaluar(solucion_actual)
        evaluaciones_gastadas: int = 1
        
        while evaluaciones_gastadas < presupuesto:
            candidato: np.ndarray = self.generar_vecino(solucion_actual)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            if valor_candidato < valor_actual:
                solucion_actual = candidato
                valor_actual = valor_candidato
                
        return solucion_actual, valor_actual



class RecocidoSimulado(AlgoritmoOptimizacion):
    """
    Permite movimientos a peores soluciones para escapar de mínimos locales.
    """

    def __init__(self, temperatura_inicial: float = 100.0, tasa_enfriamiento: float = 0.99, tamano_paso: float = 0.5) -> None:
        """
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
            
            # Si es mejor o si cumple la probabilidad, aceptamos
            if diferencia < 0 or np.random.rand() < math.exp(-diferencia / temperatura):  # .exp() = e^(-diferencia/temperatura)
                solucion_actual = candidato
                valor_actual = valor_candidato
                
                if valor_actual < mejor_valor_global:
                    mejor_solucion_global = solucion_actual.copy()
                    mejor_valor_global = valor_actual
            
            # Enfriamos el sistema
            temperatura *= self.tasa_enfriamiento
            # Evitamos división por cero por errores de precisión de punto flotante
            temperatura = max(temperatura, 1e-10) 
                
        return mejor_solucion_global, mejor_valor_global
    


class EscaladaColinasReinicios(AlgoritmoOptimizacion):
    """
    Realiza una búsqueda local, pero si se estanca (no mejora en 'N' intentos),
    reinicia la búsqueda desde un punto completamente nuevo generado al azar.
    """

    def __init__(self, tamano_paso: float = 0.5, paciencia: int = 100) -> None:
        """
        Args:
            tamano_paso (float): Magnitud de la perturbación para vecinos.
            paciencia (int): Número de intentos sin mejora antes de reiniciar.
        """

        super().__init__(nombre=f"Escalada Colinas Reinicios (paso={tamano_paso}, paciencia={paciencia})")
        self.tamano_paso: float = tamano_paso
        self.paciencia: int = paciencia

    def generar_vecino(self, solucion_actual: np.ndarray) -> np.ndarray:
        """Genera un vecino cercano aplicando un pequeño ruido."""

        ruido = np.random.uniform(-self.tamano_paso, self.tamano_paso, size=solucion_actual.shape)
        vecino = solucion_actual + ruido
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        mejor_solucion_global: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        mejor_valor_global: float = funcion.evaluar(mejor_solucion_global)
        evaluaciones_gastadas: int = 1
        
        solucion_actual: np.ndarray = mejor_solucion_global.copy()
        valor_actual: float = mejor_valor_global
        intentos_sin_mejora: int = 0
        
        while evaluaciones_gastadas < presupuesto:
            candidato: np.ndarray = self.generar_vecino(solucion_actual)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            if valor_candidato < valor_actual:
                solucion_actual = candidato
                valor_actual = valor_candidato
                intentos_sin_mejora = 0 # Reseteamos la paciencia
                
                # Actualizamos el récord global si es necesario
                if valor_actual < mejor_valor_global:
                    mejor_solucion_global = solucion_actual.copy()
                    mejor_valor_global = valor_actual
            else:
                intentos_sin_mejora += 1
                
            # Condición de reinicio si nos quedamos atascados
            if intentos_sin_mejora >= self.paciencia:
                if evaluaciones_gastadas < presupuesto:
                    solucion_actual = self.generar_punto_aleatorio(dimensiones)
                    valor_actual = funcion.evaluar(solucion_actual)
                    evaluaciones_gastadas += 1
                    intentos_sin_mejora = 0
                    
        return mejor_solucion_global, mejor_valor_global


class BusquedaLocalReiterada(AlgoritmoOptimizacion):
    """
    Búsqueda Local Reiterada (Iterated Local Search).
    Al atascarse en un óptimo local, aplica una gran perturbación (un salto) 
    para intentar escapar a un valle mejor.
    """

    def __init__(self, tamano_paso: float = 0.5, tamano_salto: float = 3.0, paciencia: int = 100) -> None:
        """
        Inicializa el algoritmo.
        
        Args:
            tamano_paso (float): Magnitud del paso para la búsqueda normal.
            tamano_salto (float): Magnitud del gran salto cuando se atasca.
            paciencia (int): Intentos sin mejora antes de dar el salto.
        """
        super().__init__(nombre=f"Búsqueda Local Reiterada (paso={tamano_paso}, salto={tamano_salto})")
        self.tamano_paso: float = tamano_paso
        self.tamano_salto: float = tamano_salto
        self.paciencia: int = paciencia

    def generar_vecino(self, solucion: np.ndarray, magnitud: float) -> np.ndarray:
        """Genera un vecino aplicando un ruido de la magnitud especificada."""
        ruido = np.random.uniform(-magnitud, magnitud, size=solucion.shape)
        vecino = solucion + ruido
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        mejor_solucion_global: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        mejor_valor_global: float = funcion.evaluar(mejor_solucion_global)
        evaluaciones_gastadas: int = 1
        
        solucion_actual: np.ndarray = mejor_solucion_global.copy()
        valor_actual: float = mejor_valor_global
        intentos_sin_mejora: int = 0
        
        while evaluaciones_gastadas < presupuesto:
            # Búsqueda local normal
            candidato: np.ndarray = self.generar_vecino(solucion_actual, self.tamano_paso)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            if valor_candidato < valor_actual:
                solucion_actual = candidato
                valor_actual = valor_candidato
                intentos_sin_mejora = 0
                
                if valor_actual < mejor_valor_global:
                    mejor_solucion_global = solucion_actual.copy()
                    mejor_valor_global = valor_actual
            else:
                intentos_sin_mejora += 1
                
            # Condición de salto grande si nos atascamos
            if intentos_sin_mejora >= self.paciencia:
                # Saltamos desde la mejor solución que hemos encontrado hasta ahora
                solucion_actual = self.generar_vecino(mejor_solucion_global, self.tamano_salto)
                if evaluaciones_gastadas < presupuesto:
                    valor_actual = funcion.evaluar(solucion_actual)
                    evaluaciones_gastadas += 1
                intentos_sin_mejora = 0
                    
        return mejor_solucion_global, mejor_valor_global
    


class EscaladaColinasDinamica(AlgoritmoOptimizacion):
    """
    NUEVO LAB 8: Escalada de Colinas con tamaño de paso dinámico.
    El tamaño del salto se reduce proporcionalmente a medida que se agota el presupuesto.
    """

    def __init__(self, paso_inicial: float = 2.0, paso_final: float = 0.01) -> None:
        """
        Inicializa el algoritmo dinámico.
        
        Args:
            paso_inicial (float): Tamaño del salto al principio (exploración amplia).
            paso_final (float): Tamaño del salto al final (explotación fina).
        """
        super().__init__(nombre=f"Escalada Colinas Dinámica (Paso: {paso_inicial} -> {paso_final})")
        self.paso_inicial: float = paso_inicial
        self.paso_final: float = paso_final

    def generar_vecino(self, solucion_actual: np.ndarray, tamano_paso_actual: float) -> np.ndarray:
        """NUEVO LAB 8: Genera un vecino usando el paso dinámico calculado."""
        ruido = np.random.uniform(-tamano_paso_actual, tamano_paso_actual, size=solucion_actual.shape)
        vecino = solucion_actual + ruido
        return np.clip(vecino, self.limite_inferior, self.limite_superior)

    def ejecutar(self, funcion: Any, presupuesto: int, dimensiones: int = 10) -> Tuple[np.ndarray, float]:
        solucion_actual: np.ndarray = self.generar_punto_aleatorio(dimensiones)
        valor_actual: float = funcion.evaluar(solucion_actual)
        evaluaciones_gastadas: int = 1
        
        # NUEVO LAB 8: Guardamos el primer valor en nuestro historial
        self.historial_convergencia.append(valor_actual)
        
        while evaluaciones_gastadas < presupuesto:
            # NUEVO LAB 8: Cálculo del paso dinámico (Decaimiento lineal)
            # Progreso va de 0.0 (inicio) a 1.0 (fin)
            progreso: float = evaluaciones_gastadas / presupuesto
            # El paso actual es una interpolación entre el inicial y el final
            paso_actual: float = self.paso_inicial - (progreso * (self.paso_inicial - self.paso_final))
            
            candidato: np.ndarray = self.generar_vecino(solucion_actual, paso_actual)
            valor_candidato: float = funcion.evaluar(candidato)
            evaluaciones_gastadas += 1
            
            if valor_candidato < valor_actual:
                solucion_actual = candidato
                valor_actual = valor_candidato
            
            # NUEVO LAB 8: Añadimos el mejor valor conocido en este momento al historial
            self.historial_convergencia.append(valor_actual)
                
        return solucion_actual, valor_actual