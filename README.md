# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

**Curso:** Programación (Código: 213023) - Fase 4 (Prácticas Simuladas)  
**Institución:** Universidad Nacional Abierta y a Distancia (UNAD)  
**Lenguaje:** Python 3.12+ (Sin dependencias externas ni motores de base de datos)

## Descripción del Proyecto
Aplicación orientada a objetos desarrollada para la empresa **Software FJ**, orientada a gestionar clientes, servicios especializados (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas. El sistema opera completamente en memoria mediante estructuras de objetos y listas internas, utilizando archivos planos exclusivamente para el registro de auditoría y errores (`registro_sistema.log`).

## Estructura del Repositorio
```text
├── excepciones.py      # Jerarquía de excepciones personalizadas de Software FJ
├── logger_sistema.py   # Configuración del registro de eventos y errores (.log)
├── modelos.py          # Clases abstractas, herencia, polimorfismo, encapsulación y sobrecarga
├── gestor.py           # Controlador de lógica de negocio y manejo avanzado de excepciones
├── main.py             # Simulación de 12 operaciones completas (válidas e inválidas)
└── README.md           # Documentación técnica del proyecto
```

## Ejecución
```bash
python main.py
```
Al ejecutar `main.py`, el sistema simulará 12 operaciones completas en consola y generará automáticamente el archivo `registro_sistema.log` con la trazabilidad detallada de eventos y excepciones encadenadas.
