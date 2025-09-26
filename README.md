Sistema de Control de Calidad Automatizado para Chocolates
Descripción
Este proyecto implementa un sistema de control de calidad automatizado para una fábrica de chocolates utilizando principios de programación orientada a objetos (POO). El sistema simula la detección de defectos en diferentes etapas del proceso productivo (moldeado y empaque) mediante sensores virtuales.

Características Principales
🏗️ Arquitectura POO
Encapsulamiento: Atributos protegidos y métodos getter para control de acceso

Herencia: Clases especializadas para diferentes tipos de chocolates

Polimorfismo: Métodos evaluar_calidad() con implementaciones específicas

Abstracción: Clase abstracta SensorCalidad para definir interfaz común

🔍 Funcionalidades
Detección automática de defectos en chocolates

Evaluación de calidad según criterios específicos por proceso

Generación de reportes estadísticos

Registro detallado de inspecciones

Estructura del Proyecto
Clases Principales
Chocolate (Clase Base)
Representa un chocolate con atributos básicos

Gestiona defectos y estado de calidad

Método base para evaluación de calidad

ChocolateMoldeado (Herencia)
Especialización para proceso de moldeado

Criterios específicos: burbujas, rotura, forma incorrecta

ChocolateEmpaque (Herencia)
Especialización para proceso de empaque

Criterios específicos: rotura, empaque dañado, pieza faltante

SensorCalidad (Clase Abstracta)
Define interfaz para sensores de calidad

Método abstracto detectar_defectos()

SensorVisual (Implementación Concreta)
Simula detección de defectos mediante visión artificial

Lógica específica para moldeado y empaque

SistemaControlCalidad
Gestiona el flujo completo de control de calidad

Registra sensores por proceso

Genera reportes estadísticos

Enumeraciones
TipoDefecto
BURBUJAS: Burbujas de aire en el chocolate

ROTURA: Chocolate roto o quebrado

FORMA_INCORRECTA: Forma no conforme al molde

MANCHAS: Manchas o imperfecciones superficiales

FALTANTE: Pieza faltante en el empaque

EMPAQUE_DANADO: Empaque dañado o defectuoso

EstadoCalidad
APROBADO: Cumple con los estándares de calidad

RECHAZADO: No cumple con los estándares

PENDIENTE: Esperando evaluación

Instalación y Uso
Requisitos
Python 3.7 o superior

No se requieren dependencias externas
