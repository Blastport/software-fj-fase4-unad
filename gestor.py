"""
Módulo: gestor.py
Descripción: Clase controladora central (GestorSoftwareFJ) que administra las listas
en memoria de clientes, servicios y reservas (sin bases de datos) y coordina el manejo
avanzado de excepciones (try/except, try/except/else, try/except/finally y encadenamiento).
"""

import logging
from typing import List, Optional

from excepciones import (
    ErrorSistemaFJ,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
)
from modelos import Cliente, Servicio, Reserva


class GestorSoftwareFJ:
    """
    Orquestador de operaciones de negocio para Software FJ.
    Mantiene el almacenamiento en listas internas y garantiza continuidad operativa ante fallos.
    """

    def __init__(self, logger: logging.Logger):
        # Listas privadas en memoria (sustituyen cualquier motor de base de datos)
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        self.__logger: logging.Logger = logger
        self.__logger.info("Sistema GestorSoftwareFJ inicializado correctamente en memoria.")

    @property
    def clientes(self) -> List[Cliente]:
        """Retorna una copia de la lista de clientes registrados."""
        return list(self.__clientes)

    @property
    def servicios(self) -> List[Servicio]:
        """Retorna una copia de la lista de servicios registrados."""
        return list(self.__servicios)

    @property
    def reservas(self) -> List[Reserva]:
        """Retorna una copia de la lista de reservas registradas."""
        return list(self.__reservas)

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        """
        Crea y registra un cliente en la lista interna utilizando bloque try / except / else.
        """
        nuevo_cliente: Optional[Cliente] = None
        try:
            # Verifica duplicidad de identificación antes de instanciar
            if any(c.id_entidad == str(id_cliente).strip() for c in self.__clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con ID '{id_cliente}'.")
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as error:
            # Registro detallado del error en el archivo de logs sin detener la aplicación
            self.__logger.error(f"Fallo al registrar cliente (ID={id_cliente}): {error}")
            return None
        else:
            # El bloque else se ejecuta únicamente si el bloque try finalizó sin excepciones
            self.__clientes.append(nuevo_cliente)
            self.__logger.info(f"Cliente registrado exitosamente -> {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """
        Agrega un servicio especializado al catálogo interno usando try / except / else.
        """
        try:
            if not isinstance(servicio, Servicio):
                raise OperacionNoPermitidaError("El objeto proporcionado no es una instancia válida de Servicio.")
            if any(s.id_entidad == servicio.id_entidad for s in self.__servicios):
                raise OperacionNoPermitidaError(f"Ya existe un servicio con ID '{servicio.id_entidad}'.")
        except ErrorSistemaFJ as error:
            self.__logger.error(f"Fallo al registrar servicio: {error}")
            return False
        else:
            self.__servicios.append(servicio)
            self.__logger.info(f"Servicio incorporado al catálogo -> {servicio.obtener_resumen()}")
            return True

    def crear_y_procesar_reserva(
        self,
        id_reserva: str,
        cliente: Optional[Cliente],
        servicio: Optional[Servicio],
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> Optional[Reserva]:
        """
        Flujo completo de reserva: creación, confirmación y liquidación financiera.
        Demuestra el uso de try / except / finally y encadenamiento de excepciones.
        """
        reserva: Optional[Reserva] = None
        self.__logger.info(f"Iniciando transacción de reserva '{id_reserva}'...")
        try:
            # 1. Validación de existencia en listas internas
            if cliente is None or cliente not in self.__clientes:
                raise ReservaInvalidaError("El cliente indicado no está registrado en el sistema.")
            if servicio is None or servicio not in self.__servicios:
                raise ReservaInvalidaError("El servicio indicado no existe en el catálogo activo.")

            # 2. Instanciación, confirmación y procesamiento de la reserva
            reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
            reserva.confirmar()
            reserva.procesar_reserva(impuesto=impuesto, descuento=descuento, cargo_extra=cargo_extra)

            # 3. Almacenamiento en la lista interna de reservas
            self.__reservas.append(reserva)
            self.__logger.info(f"Reserva procesada con éxito -> {reserva.obtener_resumen()}")
            return reserva

        except ErrorSistemaFJ as error:
            # Si existe una causa encadenada (__cause__), también se documenta en el log
            causa = f" | Causa raíz: {repr(error.__cause__)}" if error.__cause__ else ""
            self.__logger.error(f"Error controlado en reserva '{id_reserva}': {error}{causa}")
            return None
        except Exception as error_inesperado:
            # Captura de seguridad para cualquier excepción imprevista de Python con encadenamiento
            try:
                raise ReservaInvalidaError(
                    f"Error inesperado durante la reserva '{id_reserva}'."
                ) from error_inesperado
            except ReservaInvalidaError as encadenado:
                self.__logger.critical(
                    f"Excepción crítica encadenada en '{id_reserva}': {encadenado} | Causa: {repr(encadenado.__cause__)}"
                )
                return None
        finally:
            # El bloque finally garantiza que siempre se registre el cierre de la transacción
            self.__logger.debug(f"Finalizado ciclo de ejecución para la transacción '{id_reserva}'.")

    def cancelar_reserva(self, id_reserva: str, motivo: str = "Cancelación solicitada") -> bool:
        """
        Busca una reserva por ID e intenta cancelarla controlando operaciones no permitidas.
        """
        try:
            reserva = next((r for r in self.__reservas if r.id_entidad == id_reserva), None)
            if reserva is None:
                raise ReservaInvalidaError(f"No se encontró ninguna reserva con ID '{id_reserva}'.")
            reserva.cancelar(motivo)
        except ErrorSistemaFJ as error:
            self.__logger.warning(f"No se pudo cancelar la reserva '{id_reserva}': {error}")
            return False
        else:
            self.__logger.info(f"Reserva '{id_reserva}' cancelada correctamente. Motivo: {motivo}.")
            return True
