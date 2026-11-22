"""
Módulo: main.py
Descripción: Punto de entrada principal del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de Software FJ (UNAD - Programación 213023 - Fase 4).
Ejecuta una simulación de 12 operaciones completas (válidas e inválidas) demostrando
estabilidad, polimorfismo, sobrecarga y manejo avanzado de excepciones sin base de datos.
"""

from excepciones import ErrorSistemaFJ
from logger_sistema import configurar_logger
from modelos import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
)
from gestor import GestorSoftwareFJ


def ejecutar_simulacion() -> None:
    """Ejecuta las 12 operaciones de prueba exigidas y muestra el reporte en consola."""
    archivo_log = "registro_sistema.log"
    logger = configurar_logger(archivo_log)
    gestor = GestorSoftwareFJ(logger)

    print("=" * 80)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro exitoso de Cliente 1
    # -------------------------------------------------------------------------
    print("\n[Operación 1] Registrando cliente válido (Carlos Mendoza)...")
    cliente_1 = gestor.registrar_cliente("1085245901", "Carlos Mendoza", "carlos.mendoza@correo.com", "3104567890")
    print("  -> Resultado:", cliente_1.obtener_resumen() if cliente_1 else "Falló")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro exitoso de Cliente 2
    # -------------------------------------------------------------------------
    print("\n[Operación 2] Registrando cliente válido (Laura Gómez)...")
    cliente_2 = gestor.registrar_cliente("1098765432", "Laura Gómez", "laura.gomez@empresa.co", "3209876543")
    print("  -> Resultado:", cliente_2.obtener_resumen() if cliente_2 else "Falló")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Intento inválido de Cliente (Correo mal formado y teléfono corto)
    # -------------------------------------------------------------------------
    print("\n[Operación 3] Intentando registrar cliente con correo inválido...")
    cliente_inv_1 = gestor.registrar_cliente("1022334455", "Andrés Pérez", "andres.sin.arroba.com", "3001112233")
    print("  -> Resultado controlado (esperado None):", cliente_inv_1)

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Intento inválido de Cliente (Parámetro obligatorio vacío)
    # -------------------------------------------------------------------------
    print("\n[Operación 4] Intentando registrar cliente con nombre vacío...")
    cliente_inv_2 = gestor.registrar_cliente("1033445566", "", "vacio@correo.com", "3150009988")
    print("  -> Resultado controlado (esperado None):", cliente_inv_2)

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación y registro exitoso de Servicio 1 (Reserva de Sala)
    # -------------------------------------------------------------------------
    print("\n[Operación 5] Creando servicio especializado: Reserva de Sala...")
    sala_juntas = ReservaSala(
        id_servicio="SRV-001",
        nombre_servicio="Sala Ejecutiva Innovación",
        tarifa_base=80000.0,
        capacidad_personas=16,
        incluye_proyector=True,
        disponible=True,
    )
    gestor.registrar_servicio(sala_juntas)
    print("  -> Resultado:", sala_juntas.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Creación y registro exitoso de Servicio 2 (Alquiler de Equipos)
    # -------------------------------------------------------------------------
    print("\n[Operación 6] Creando servicio especializado: Alquiler de Equipos...")
    equipos_dev = AlquilerEquipo(
        id_servicio="SRV-002",
        nombre_servicio="Estaciones Workstation Dell",
        tarifa_base=35000.0,
        tipo_equipo="Portátil Core i9 32GB RAM",
        cantidad_equipos=4,
        disponible=True,
    )
    gestor.registrar_servicio(equipos_dev)
    print("  -> Resultado:", equipos_dev.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Creación y registro exitoso de Servicio 3 (Asesoría Especializada)
    # -------------------------------------------------------------------------
    print("\n[Operación 7] Creando servicio especializado: Asesoría Especializada...")
    asesoria_cloud = AsesoriaEspecializada(
        id_servicio="SRV-003",
        nombre_servicio="Auditoría de Arquitectura Cloud",
        tarifa_base=120000.0,
        area_especialidad="Ciberseguridad y Nube",
        nivel_consultor="SENIOR",
        disponible=True,
    )
    gestor.registrar_servicio(asesoria_cloud)
    print("  -> Resultado:", asesoria_cloud.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Creación inválida de Servicio (Tarifa negativa y captura directa)
    # -------------------------------------------------------------------------
    print("\n[Operación 8] Intentando crear servicio con tarifa negativa (-45000)...")
    try:
        servicio_erroneo = ReservaSala(
            id_servicio="SRV-ERR",
            nombre_servicio="Sala Defectuosa",
            tarifa_base=-45000.0,
            capacidad_personas=10,
        )
        gestor.registrar_servicio(servicio_erroneo)
    except ErrorSistemaFJ as err:
        logger.error(f"Excepción capturada al instanciar servicio inválido: {err}")
        print(f"  -> Error capturado sin detener el sistema: {err}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa 1 (Sala con sobrecarga estándar: solo duración)
    # -------------------------------------------------------------------------
    print("\n[Operación 9] Procesando reserva exitosa de Sala (4 horas, IVA por defecto 19%)...")
    res_1 = gestor.crear_y_procesar_reserva(
        id_reserva="RES-101",
        cliente=cliente_1,
        servicio=sala_juntas,
        duracion_horas=4,
    )
    print("  -> Resultado:", res_1.obtener_resumen() if res_1 else "Falló")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva exitosa 2 (Asesoría con descuento 10% y cargo extra)
    # -------------------------------------------------------------------------
    print("\n[Operación 10] Procesando reserva exitosa de Asesoría (3 horas, 10% dto + $20,000 extra)...")
    res_2 = gestor.crear_y_procesar_reserva(
        id_reserva="RES-102",
        cliente=cliente_2,
        servicio=asesoria_cloud,
        duracion_horas=3,
        impuesto=0.19,
        descuento=0.10,
        cargo_extra=20000.0,
    )
    print("  -> Resultado:", res_2.obtener_resumen() if res_2 else "Falló")

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva exitosa 3 (Alquiler de Equipos) + Intento de cancelación inválida
    # -------------------------------------------------------------------------
    print("\n[Operación 11] Procesando reserva de Equipos e intentando cancelarla tras ser procesada...")
    res_3 = gestor.crear_y_procesar_reserva(
        id_reserva="RES-103",
        cliente=cliente_1,
        servicio=equipos_dev,
        duracion_horas=5,
        descuento=0.05,
    )
    print("  -> Reserva creada:", res_3.obtener_resumen() if res_3 else "Falló")
    cancelada = gestor.cancelar_reserva("RES-103", "Cambio de planes")
    print("  -> ¿Se permitió cancelar reserva ya procesada?:", cancelada)

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Reserva fallida con Encadenamiento de Excepciones (Descuento 150% y Servicio No Disponible)
    # -------------------------------------------------------------------------
    print("\n[Operación 12] Probando reserva con descuento inconsistente (150%) y servicio inactivo...")
    res_fallida_calc = gestor.crear_y_procesar_reserva(
        id_reserva="RES-104",
        cliente=cliente_2,
        servicio=sala_juntas,
        duracion_horas=2,
        descuento=1.50,  # Dispara CalculoInconsistenteError encadenado a ReservaInvalidaError
    )
    print("  -> Resultado reserva con descuento 150% (esperado None):", res_fallida_calc)

    # Servicio marcado como no disponible
    servicio_inactivo = AlquilerEquipo(
        id_servicio="SRV-004",
        nombre_servicio="Servidor Rack Xeon",
        tarifa_base=90000.0,
        tipo_equipo="Servidor Dedicado",
        cantidad_equipos=1,
        disponible=False,
    )
    gestor.registrar_servicio(servicio_inactivo)
    res_fallida_disp = gestor.crear_y_procesar_reserva(
        id_reserva="RES-105",
        cliente=cliente_1,
        servicio=servicio_inactivo,
        duracion_horas=6,
    )
    print("  -> Resultado reserva servicio no disponible (esperado None):", res_fallida_disp)

    # -------------------------------------------------------------------------
    # RESUMEN FINAL DEL ESTADO EN MEMORIA
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("RESUMEN FINAL DE ENTIDADES EN MEMORIA (SIN BASE DE DATOS)")
    print("=" * 80)
    print(f"Total Clientes válidos registrados : {len(gestor.clientes)}")
    print(f"Total Servicios en catálogo        : {len(gestor.servicios)}")
    print(f"Total Reservas exitosas procesadas : {len(gestor.reservas)}")
    print(f"Archivo de auditoría generado      : {archivo_log}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_simulacion()
