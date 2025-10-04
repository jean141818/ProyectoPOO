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
        if not self._resultados:
            return "No hay datos de inspección para generar reporte."
        
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
        
        if contador_defectos:
            for defecto, count in contador_defectos.items():
                reporte += f"  - {defecto}: {count} ocurrencias\n"
        else:
            reporte += "  No se detectaron defectos\n"
        
        return reporte
    
    def mostrar_inspecciones(self) -> str:
        """Muestra el historial de inspecciones"""
        if not self._resultados:
            return "No hay inspecciones registradas."
        
        reporte = "HISTORIAL DE INSPECCIONES\n"
        reporte += "=" * 50 + "\n"
        
        for i, resultado in enumerate(self._resultados, 1):
            reporte += f"{i}. Lote: {resultado['lote_id']} | "
            reporte += f"Proceso: {resultado['proceso']} | "
            reporte += f"Resultado: {resultado['resultado']}\n"
            if resultado['defectos']:
                reporte += f"   Defectos: {', '.join(resultado['defectos'])}\n"
            reporte += f"   Fecha: {resultado['fecha'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            reporte += "-" * 50 + "\n"
        
        return reporte

# Función para mostrar el menú principal
def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "=" * 50)
    print("    SISTEMA DE CONTROL DE CALIDAD - CHOCOLATES")
    print("=" * 50)
    print("1. Inspeccionar chocolate de moldeado")
    print("2. Inspeccionar chocolate de empaque")
    print("3. Proceso completo (moldeado + empaque)")
    print("4. Generar reporte de calidad")
    print("5. Mostrar historial de inspecciones")
    print("6. Simular producción en lote")
    print("7. Salir")
    print("-" * 50)

# Función para obtener entrada del usuario
def obtener_opcion():
    """Obtiene y valida la opción del usuario"""
    try:
        opcion = int(input("Seleccione una opción (1-7): "))
        return opcion
    except ValueError:
        print("Error: Por favor ingrese un número válido.")
        return -1

# Función para simular producción en lote
def simular_produccion_lote(sistema: SistemaControlCalidad, cantidad: int):
    """Simula la producción y control de calidad de múltiples chocolates"""
    print(f"\nSimulando producción de {cantidad} chocolates...")
    
    for i in range(cantidad):
        # Crear chocolate para moldeado
        chocolate_molde = ChocolateMoldeado(f"LOTE-M-{i+1}", datetime.now(), "corazon")
        resultado_molde = sistema.inspeccionar_chocolate(chocolate_molde, "moldeado")
        print(f"  Moldeado {chocolate_molde.lote_id}: {resultado_molde.value}")
        
        # Si pasa moldeado, proceder a empaque
        if resultado_molde == EstadoCalidad.APROBADO:
            chocolate_empaque = ChocolateEmpaque(f"LOTE-E-{i+1}", datetime.now(), "caja_regalo")
            resultado_empaque = sistema.inspeccionar_chocolate(chocolate_empaque, "empaque")
            print(f"  Empaque {chocolate_empaque.lote_id}: {resultado_empaque.value}")
        else:
            print(f"  ❌ Chocolate {chocolate_molde.lote_id} rechazado en moldeado")

# Programa principal con menú interactivo
def main():
    # Crear sistema de control de calidad
    sistema = SistemaControlCalidad()
    
    # Registrar sensores para cada proceso
    sensor_visual = SensorVisual()
    sistema.registrar_sensor("moldeado", sensor_visual)
    sistema.registrar_sensor("empaque", sensor_visual)
    
    print("Sistema de Control de Calidad Inicializado")
    print("Sensores registrados: Moldeado y Empaque")
    
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        
        if opcion == 1:
            # Inspeccionar chocolate de moldeado
            lote_id = input("Ingrese ID del lote para moldeado: ")
            chocolate = ChocolateMoldeado(lote_id, datetime.now(), "corazon")
            resultado = sistema.inspeccionar_chocolate(chocolate, "moldeado")
            print(f"\n✅ Resultado: {resultado.value}")
            if chocolate.defectos:
                print(f"❌ Defectos detectados: {[d.value for d in chocolate.defectos]}")
        
        elif opcion == 2:
            # Inspeccionar chocolate de empaque
            lote_id = input("Ingrese ID del lote para empaque: ")
            chocolate = ChocolateEmpaque(lote_id, datetime.now(), "caja_regalo")
            resultado = sistema.inspeccionar_chocolate(chocolate, "empaque")
            print(f"\n✅ Resultado: {resultado.value}")
            if chocolate.defectos:
                print(f"❌ Defectos detectados: {[d.value for d in chocolate.defectos]}")
        
        elif opcion == 3:
            # Proceso completo
            lote_id = input("Ingrese ID del lote: ")
            
            # Moldeado
            chocolate_molde = ChocolateMoldeado(f"{lote_id}-M", datetime.now(), "corazon")
            resultado_molde = sistema.inspeccionar_chocolate(chocolate_molde, "moldeado")
            print(f"\n🔧 Moldeado: {resultado_molde.value}")
            
            if resultado_molde == EstadoCalidad.APROBADO:
                # Empaque
                chocolate_empaque = ChocolateEmpaque(f"{lote_id}-E", datetime.now(), "caja_regalo")
                resultado_empaque = sistema.inspeccionar_chocolate(chocolate_empaque, "empaque")
                print(f"📦 Empaque: {resultado_empaque.value}")
                
                if resultado_empaque == EstadoCalidad.APROBADO:
                    print("🎉 ¡Producto final APROBADO!")
                else:
                    print("❌ Producto rechazado en empaque")
            else:
                print("❌ Producto rechazado en moldeado")
        
        elif opcion == 4:
            # Generar reporte
            print(sistema.generar_reporte())
        
        elif opcion == 5:
            # Mostrar historial
            print(sistema.mostrar_inspecciones())
        
        elif opcion == 6:
            # Simular producción en lote
            try:
                cantidad = int(input("Ingrese cantidad de chocolates a producir: "))
                if cantidad > 0:
                    simular_produccion_lote(sistema, cantidad)
                    print(f"\n✅ Simulación completada: {cantidad} chocolates procesados")
                else:
                    print("❌ La cantidad debe ser mayor a 0")
            except ValueError:
                print("❌ Error: Ingrese un número válido")
        
        elif opcion == 7:
            # Salir
            print("\n¡Gracias por usar el Sistema de Control de Calidad!")
            break
        
        else:
            print("❌ Opción inválida. Por favor seleccione 1-7.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
