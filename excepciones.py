"""
Módulo: excepciones.py
Descripción: Define la jerarquía de excepciones personalizadas para el sistema
de gestión de clientes, servicios y reservas de la empresa Software FJ.
Permite clasificar los errores de negocio y mantener la estabilidad del sistema.
"""


class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas de Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-GEN"):
        # Se almacena el código interno del error para facilitar la auditoría en el log
        self.codigo_error = codigo_error
        # Se invoca el constructor de la clase padre Exception con el mensaje formateado
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con el formato o rango esperado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATOS")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro obligatorio es nulo, vacío o fue omitido."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-PARAM")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar ejecutar una acción inválida según el estado actual."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-OPER")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un fallo durante la creación, confirmación o cancelación de una reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RESV")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin disponibilidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERV")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando los parámetros financieros (impuestos, descuentos, totales) son incoherentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALC")
