from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

class TipoDefecto(Enum):
    """Enumeración de tipos de defectos posibles"""
    BURBUJAS = "burbujas_aire"
    ROTURA = "rotura"
    FORMA_INCORRECTA = "forma_incorrecta"
    MANCHAS = "manchas"
    FALTANTE = "pieza_faltante"
    EMPAQUE_DANADO = "empaque_danado"

class EstadoCalidad(Enum):
    """Enumeración de estados de calidad"""
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"

class Chocolate:
    """Clase base que representa un chocolate con sus atributos básicos"""
    
    def __init__(self, lote_id: str, fecha_produccion: datetime):
        self._lote_id = lote_id  # Encapsulamiento: atributo protegido
        self._fecha_produccion = fecha_produccion
        self._defectos: List[TipoDefecto] = []
        self._estado_calidad = EstadoCalidad.PENDIENTE
    
    @property
    def lote_id(self) -> str:
        """Getter para lote_id (encapsulamiento)"""
        return self._lote_id
    
    @property
    def defectos(self) -> List[TipoDefecto]:
        """Getter para defectos (encapsulamiento)"""
        return self._defectos.copy()  # Devolver copia para evitar modificación externa
    
    def agregar_defecto(self, defecto: TipoDefecto) -> None:
        """Método para agregar defectos al chocolate"""
        if defecto not in self._defectos:
            self._defectos.append(defecto)
    
    def evaluar_calidad(self) -> EstadoCalidad:
        """Método base para evaluar calidad"""
        if not self._defectos:
            self._estado_calidad = EstadoCalidad.APROBADO
        else:
            self._estado_calidad = EstadoCalidad.RECHAZADO
        return self._estado_calidad
    
    def __str__(self) -> str:
        return f"Chocolate Lote {self._lote_id} - Estado: {self._estado_calidad.value}"

class ChocolateMoldeado(Chocolate):
    """Clase para chocolates del proceso de moldeado (herencia de Chocolate)"""
    
    def __init__(self, lote_id: str, fecha_produccion: datetime, tipo_molde: str):
        super().__init__(lote_id, fecha_produccion)
        self._tipo_molde = tipo_molde  # Encapsulamiento
    
    def evaluar_calidad(self) -> EstadoCalidad:
        """Polimorfismo: implementación específica para moldeado"""
        # Criterios específicos de moldeado
        if (TipoDefecto.BURBUJAS in self._defectos or 
            TipoDefecto.ROTURA in self._defectos or
            TipoDefecto.FORMA_INCORRECTA in self._defectos):
            self._estado_calidad = EstadoCalidad.RECHAZADO
        else:
            self._estado_calidad = EstadoCalidad.APROBADO
        return self._estado_calidad

class ChocolateEmpaque(Chocolate):
    """Clase para chocolates del proceso de empaque (herencia de Chocolate)"""
    
    def __init__(self, lote_id: str, fecha_produccion: datetime, tipo_empaque: str):
        super().__init__(lote_id, fecha_produccion)
        self._tipo_empaque = tipo_empaque
    
    def evaluar_calidad(self) -> EstadoCalidad:
        """Polimorfismo: implementación específica para empaque"""
        # Criterios específicos de empaque
        if (TipoDefecto.ROTURA in self._defectos or 
            TipoDefecto.EMPAQUE_DANADO in self._defectos or
            TipoDefecto.FALTANTE in self._defectos):
            self._estado_calidad = EstadoCalidad.RECHAZADO
        else:
            self._estado_calidad = EstadoCalidad.APROBADO
        return self._estado_calidad

class SensorCalidad(ABC):
    """Clase abstracta para sensores de calidad (abstracción)"""
    
    @abstractmethod
    def detectar_defectos(self, chocolate: Chocolate) -> List[TipoDefecto]:
        """Método abstracto para detección de defectos"""
        pass

class SensorVisual(SensorCalidad):
    """Sensor visual para detección de defectos (implementación concreta)"""
    
    def detectar_defectos(self, chocolate: Chocolate) -> List[TipoDefecto]:
        """Simula detección de defectos mediante visión artificial"""
        # En una implementación real, aquí iría la lógica de computer vision
        defectos_detectados = []
        
        # Simulación de detección (lógica de ejemplo)
        if isinstance(chocolate, ChocolateMoldeado):
            # Lógica específica para moldeado
            defectos_detectados.extend(self._analizar_moldeado())
        
        elif isinstance(chocolate, ChocolateEmpaque):
            # Lógica específica para empaque
            defectos_detectados.extend(self._analizar_empaque())
        
        return defectos_detectados
    
    def _analizar_moldeado(self) -> List[TipoDefecto]:
        """Método privado para análisis de moldeado (encapsulamiento)"""
        # Simulación de análisis de imágenes
        import random
        defectos_posibles = [TipoDefecto.BURBUJAS, TipoDefecto.ROTURA, 
                           TipoDefecto.FORMA_INCORRECTA, TipoDefecto.MANCHAS]
        return random.choices(defectos_posibles, k=random.randint(0, 2))
    
    def _analizar_empaque(self) -> List[TipoDefecto]:
        """Método privado para análisis de empaque (encapsulamiento)"""
        import random
        defectos_posibles = [TipoDefecto.ROTURA, TipoDefecto.EMPAQUE_DANADO, 
                           TipoDefecto.FALTANTE]
        return random.choices(defectos_posibles, k=random.randint(0, 1))

class SistemaControlCalidad:
    """Sistema principal que gestiona el control de calidad automatizado"""
    
    def __init__(self):
        self._sensores: Dict[str, SensorCalidad] = {}  # Encapsulamiento
        self._resultados: List[Dict] = []
    
    def registrar_sensor(self, proceso: str, sensor: SensorCalidad) -> None:
        """Registra un sensor para un proceso específico"""
        self._sensores[proceso] = sensor
    
    def inspeccionar_chocolate(self, chocolate: Chocolate, proceso: str) -> EstadoCalidad:
        """Realiza la inspección automática de un chocolate"""
        if proceso not in self._sensores:
            raise ValueError(f"No hay sensor registrado para el proceso: {proceso}")
        
        sensor = self._sensores[proceso]
        defectos = sensor.detectar_defectos(chocolate)
        
        # Agregar defectos detectados al chocolate
        for defecto in defectos:
            chocolate.agregar_defecto(defecto)
        
        # Evaluar calidad (polimorfismo: se usa la implementación específica)
        resultado = chocolate.evaluar_calidad()
        
        # Registrar resultado
        self._registrar_resultado(chocolate, defectos, resultado, proceso)
        
        return resultado
    
    def _registrar_resultado(self, chocolate: Chocolate, defectos: List[TipoDefecto], 
                           resultado: EstadoCalidad, proceso: str) -> None:
        """Método privado para registrar resultados (encapsulamiento)"""
        registro = {
            'lote_id': chocolate.lote_id,
            'fecha': datetime.now(),
            'proceso': proceso,
            'defectos': [d.value for d in defectos],
            'resultado': resultado.value,
            'tipo_chocolate': chocolate.__class__.__name__
        }
        self._resultados.append(registro)
    
    def generar_reporte(self) -> str:
        """Genera un reporte de calidad"""
        total_inspecciones = len(self._resultados)
        aprobados = sum(1 for r in self._resultados if r['resultado'] == EstadoCalidad.APROBADO.value)
        tasa_aprobacion = (aprobados / total_inspecciones * 100) if total_inspecciones > 0 else 0
        
        reporte = f"""
        REPORTE DE CONTROL DE CALIDAD
        =============================
        Total de inspecciones: {total_inspecciones}
        Productos aprobados: {aprobados}
        Productos rechazados: {total_inspecciones - aprobados}
        Tasa de aprobación: {tasa_aprobacion:.2f}%
        
        Detalle por defectos:
        """
        
        # Contar defectos por tipo
        contador_defectos = {}
        for resultado in self._resultados:
            for defecto in resultado['defectos']:
                contador_defectos[defecto] = contador_defectos.get(defecto, 0) + 1
        
        for defecto, count in contador_defectos.items():
            reporte += f"  - {defecto}: {count} ocurrencias\n"
        
        return reporte

# Ejemplo de uso del sistema
def main():
    # Crear sistema de control de calidad
    sistema = SistemaControlCalidad()
    
    # Registrar sensores para cada proceso
    sensor_visual = SensorVisual()
    sistema.registrar_sensor("moldeado", sensor_visual)
    sistema.registrar_sensor("empaque", sensor_visual)
    
    # Simular producción y control de calidad
    for i in range(10):
        # Crear chocolates para moldeado
        chocolate_molde = ChocolateMoldeado(f"LOTE-M-{i+1}", datetime.now(), "corazon")
        resultado_molde = sistema.inspeccionar_chocolate(chocolate_molde, "moldeado")
        print(f"Moldeado {chocolate_molde.lote_id}: {resultado_molde.value}")
        
        # Si pasa moldeado, proceder a empaque
        if resultado_molde == EstadoCalidad.APROBADO:
            chocolate_empaque = ChocolateEmpaque(f"LOTE-E-{i+1}", datetime.now(), "caja_regalo")
            resultado_empaque = sistema.inspeccionar_chocolate(chocolate_empaque, "empaque")
            print(f"Empaque {chocolate_empaque.lote_id}: {resultado_empaque.value}")
    
    # Generar reporte final
    print(sistema.generar_reporte())

if __name__ == "__main__":
    main()