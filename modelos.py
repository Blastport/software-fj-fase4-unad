"""
Módulo: modelos.py
Descripción: Contiene las clases abstractas y concretas del dominio de Software FJ.
Implementa abstracción, herencia, polimorfismo, encapsulación y métodos sobrecargados.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import overload, Optional

from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad general dentro de Software FJ.
    Define la estructura mínima de identificación, fecha de registro y contratos obligatorios.
    """

    def __init__(self, id_entidad: str):
        # Validación inicial del identificador de la entidad
        if id_entidad is None or str(id_entidad).strip() == "":
            raise ParametroFaltanteError("El identificador de la entidad no puede estar vacío.")
        # Atributos privados (encapsulación estricta)
        self.__id_entidad: str = str(id_entidad).strip()
        self.__fecha_registro: datetime = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self.__id_entidad

    @property
    def fecha_registro(self) -> str:
        """Retorna la fecha y hora de creación en formato legible."""
        return self.__fecha_registro.strftime("%Y-%m-%d %H:%M:%S")

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que obliga a las clases hijas a validar su estado interno."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que retorna una representación descriptiva de la entidad."""
        pass


class Cliente(EntidadSistema):
    """
    Representa a un cliente registrado en Software FJ.
    Encapsula sus datos personales y aplica validaciones estrictas en cada propiedad.
    """

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Se invoca el constructor de la clase abstracta EntidadSistema
        super().__init__(id_cliente)
        # Se asignan los atributos mediante los setters para ejecutar las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Se ejecuta la validación integral del objeto creado
        self.validar()

    @property
    def nombre(self) -> str:
        """Obtiene el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        texto = str(valor).strip()
        if len(texto) < 3 or any(char.isdigit() for char in texto):
            raise DatosInvalidosError(
                f"Nombre inválido ('{texto}'): debe tener al menos 3 letras y no contener números."
            )
        self.__nombre = texto

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato estándar de correo electrónico y lo asigna."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        texto = str(valor).strip()
        patron_correo = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron_correo, texto):
            raise DatosInvalidosError(f"Formato de correo electrónico inválido: '{texto}'.")
        self.__correo = texto.lower()

    @property
    def telefono(self) -> str:
        """Obtiene el número telefónico del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga exactamente 10 dígitos numéricos."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise DatosInvalidosError(
                f"Teléfono inválido ('{texto}'): debe contener exactamente 10 dígitos numéricos."
            )
        self.__telefono = texto

    def validar(self) -> bool:
        """Verifica que la identificación y los datos personales del cliente sean íntegros."""
        if not self.id_entidad.isdigit() or len(self.id_entidad) < 6:
            raise DatosInvalidosError(
                f"Identificación de cliente inválida ('{self.id_entidad}'): debe ser numérica de mínimo 6 dígitos."
            )
        return True

    def obtener_resumen(self) -> str:
        """Implementación polimórfica que devuelve los datos formateados del cliente."""
        return (
            f"Cliente [ID: {self.id_entidad}] | Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )


class Servicio(EntidadSistema, ABC):
    """
    Clase abstracta que modela un servicio ofrecido por Software FJ.
    Define el contrato polimórfico para el cálculo de costos (con métodos sobrecargados)
    y la descripción específica de cada tipo de servicio.
    """

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        # Inicializa la entidad base
        super().__init__(id_servicio)
        # Encapsulación mediante propiedades validadas
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre_servicio(self) -> str:
        """Retorna el nombre comercial del servicio."""
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self.__nombre_servicio = str(valor).strip()

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por hora del servicio."""
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as exc:
            # Encadenamiento de excepción al fallar la conversión numérica
            raise DatosInvalidosError(f"La tarifa base '{valor}' debe ser un valor numérico.") from exc

        if tarifa <= 0:
            raise DatosInvalidosError(f"La tarifa base debe ser mayor a cero (recibido: {tarifa}).")
        self.__tarifa_base = tarifa

    @property
    def disponible(self) -> bool:
        """Indica si el servicio se encuentra habilitado para ser reservado."""
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise DatosInvalidosError("El estado de disponibilidad debe ser booleano (True/False).")
        self.__disponible = estado

    def _validar_parametros_calculo(self, duracion_horas: float, impuesto: float, descuento: float, cargo_extra: float) -> None:
        """Método protegido auxiliar para verificar consistencia financiera antes de calcular costos."""
        if duracion_horas <= 0:
            raise CalculoInconsistenteError(f"La duración en horas debe ser positiva (recibido: {duracion_horas}).")
        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError(f"El impuesto debe estar entre 0.0 y 1.0 (recibido: {impuesto}).")
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError(
                f"El descuento debe estar entre 0.0 y 0.99 (recibido: {descuento})."
            )
        if cargo_extra < 0:
            raise CalculoInconsistenteError(f"El cargo adicional no puede ser negativo (recibido: {cargo_extra}).")

    # --- Declaraciones de sobrecarga (@overload) para el método calcular_costo ---
    @overload
    def calcular_costo(self, duracion_horas: float) -> float: ...

    @overload
    def calcular_costo(self, duracion_horas: float, impuesto: float) -> float: ...

    @overload
    def calcular_costo(self, duracion_horas: float, impuesto: float, descuento: float) -> float: ...

    @overload
    def calcular_costo(
        self, duracion_horas: float, impuesto: float, descuento: float, cargo_extra: float
    ) -> float: ...

    @abstractmethod
    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> float:
        """
        Método abstracto y sobrecargado para calcular el costo total del servicio.
        Soporta múltiples variantes: solo duración, con impuesto, con descuento y/o cargo adicional.
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto que describe las características técnicas del servicio."""
        pass

    def obtener_resumen(self) -> str:
        """Implementa el resumen general de la entidad apoyándose en el polimorfismo."""
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return f"[{self.id_entidad}] {self.describir_servicio()} | Tarifa Base: ${self.tarifa_base:,.2f}/h | Estado: {estado_txt}"


class ReservaSala(Servicio):
    """
    Servicio especializado 1: Reserva de salas tecnológicas y de reuniones.
    """

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base: float,
        capacidad_personas: int,
        incluye_proyector: bool = True,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        self.capacidad_personas = capacidad_personas
        self.incluye_proyector = incluye_proyector
        self.validar()

    @property
    def capacidad_personas(self) -> int:
        return self.__capacidad_personas

    @capacidad_personas.setter
    def capacidad_personas(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 2 or valor > 100:
            raise DatosInvalidosError(
                f"Capacidad de sala inválida ({valor}): debe ser un entero entre 2 y 100 personas."
            )
        self.__capacidad_personas = valor

    @property
    def incluye_proyector(self) -> bool:
        return self.__incluye_proyector

    @incluye_proyector.setter
    def incluye_proyector(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatosInvalidosError("El indicador de proyector debe ser booleano.")
        self.__incluye_proyector = valor

    def validar(self) -> bool:
        """Valida las reglas específicas de las salas de Software FJ."""
        if self.capacidad_personas > 30 and self.tarifa_base < 50000:
            raise DatosInvalidosError(
                "Una sala con capacidad superior a 30 personas no puede tener tarifa menor a $50,000."
            )
        return True

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> float:
        """
        Calcula el costo de la sala. Si incluye proyector, aplica un recargo fijo de equipamiento
        de $15,000 antes de impuestos y descuentos.
        """
        self._validar_parametros_calculo(duracion_horas, impuesto, descuento, cargo_extra)
        subtotal = self.tarifa_base * duracion_horas
        if self.incluye_proyector:
            subtotal += 15000.0
        subtotal += cargo_extra
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        proyector_txt = "Con Proyector 4K" if self.incluye_proyector else "Sin Proyector"
        return f"Sala '{self.nombre_servicio}' (Capacidad: {self.capacidad_personas} pers., {proyector_txt})"


class AlquilerEquipo(Servicio):
    """
    Servicio especializado 2: Alquiler de hardware y estaciones de cómputo.
    """

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base: float,
        tipo_equipo: str,
        cantidad_equipos: int,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        self.tipo_equipo = tipo_equipo
        self.cantidad_equipos = cantidad_equipos
        self.validar()

    @property
    def tipo_equipo(self) -> str:
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("Debe especificar el tipo de equipo a alquilar.")
        self.__tipo_equipo = str(valor).strip()

    @property
    def cantidad_equipos(self) -> int:
        return self.__cantidad_equipos

    @cantidad_equipos.setter
    def cantidad_equipos(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 1 or valor > 50:
            raise DatosInvalidosError(
                f"Cantidad de equipos inválida ({valor}): debe estar entre 1 y 50 unidades."
            )
        self.__cantidad_equipos = valor

    def validar(self) -> bool:
        """Valida que el inventario solicitado sea coherente."""
        return self.cantidad_equipos >= 1

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> float:
        """
        Calcula el costo multiplicando tarifa por hora y por la cantidad de equipos alquilados.
        """
        self._validar_parametros_calculo(duracion_horas, impuesto, descuento, cargo_extra)
        subtotal = (self.tarifa_base * self.cantidad_equipos * duracion_horas) + cargo_extra
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        return f"Alquiler '{self.nombre_servicio}' ({self.cantidad_equipos}x {self.tipo_equipo})"


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado 3: Consultoría y asesoría en ingeniería de software.
    """

    NIVELES_VALIDOS = ("JUNIOR", "SEMI-SENIOR", "SENIOR", "ARQUITECTO")

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_base: float,
        area_especialidad: str,
        nivel_consultor: str,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        self.area_especialidad = area_especialidad
        self.nivel_consultor = nivel_consultor
        self.validar()

    @property
    def area_especialidad(self) -> str:
        return self.__area_especialidad

    @area_especialidad.setter
    def area_especialidad(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El área de especialidad de la asesoría es obligatoria.")
        self.__area_especialidad = str(valor).strip()

    @property
    def nivel_consultor(self) -> str:
        return self.__nivel_consultor

    @nivel_consultor.setter
    def nivel_consultor(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nivel del consultor es obligatorio.")
        nivel = str(valor).strip().upper()
        if nivel not in self.NIVELES_VALIDOS:
            raise DatosInvalidosError(
                f"Nivel de consultor inválido ('{valor}'). Valores permitidos: {self.NIVELES_VALIDOS}."
            )
        self.__nivel_consultor = nivel

    def validar(self) -> bool:
        """Valida coherencia entre nivel de seniority y tarifa mínima."""
        if self.nivel_consultor == "ARQUITECTO" and self.tarifa_base < 100000:
            raise DatosInvalidosError(
                "Una asesoría de nivel ARQUITECTO requiere una tarifa base mínima de $100,000/h."
            )
        return True

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> float:
        """
        Calcula el costo de la asesoría aplicando un factor según el nivel del consultor:
        SENIOR (+15%) y ARQUITECTO (+30%).
        """
        self._validar_parametros_calculo(duracion_horas, impuesto, descuento, cargo_extra)
        multiplicador = 1.0
        if self.nivel_consultor == "SENIOR":
            multiplicador = 1.15
        elif self.nivel_consultor == "ARQUITECTO":
            multiplicador = 1.30

        subtotal = (self.tarifa_base * multiplicador * duracion_horas) + cargo_extra
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        return f"Asesoría '{self.nombre_servicio}' (Área: {self.area_especialidad} | Nivel: {self.nivel_consultor})"


class Reserva(EntidadSistema):
    """
    Clase que vincula un Cliente con un Servicio durante una duración específica,
    gestionando su ciclo de vida (PENDIENTE -> CONFIRMADA -> PROCESADA / CANCELADA).
    """

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(id_reserva)
        # Validación de tipos de objetos recibidos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere una instancia válida de Cliente para crear la reserva.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere una instancia válida de Servicio para crear la reserva.")

        self.__cliente: Cliente = cliente
        self.__servicio: Servicio = servicio
        self.duracion_horas = duracion_horas
        self.__estado: str = "PENDIENTE"
        self.__costo_final: float = 0.0
        self.validar()

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @duracion_horas.setter
    def duracion_horas(self, valor: float) -> None:
        try:
            horas = float(valor)
        except (TypeError, ValueError) as exc:
            raise DatosInvalidosError(f"La duración '{valor}' no es un número válido.") from exc

        if horas <= 0 or horas > 240:
            raise DatosInvalidosError(
                f"Duración inválida ({horas} h): debe ser mayor a 0 y máximo 240 horas."
            )
        self.__duracion_horas = horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_final(self) -> float:
        return self.__costo_final

    def validar(self) -> bool:
        """Verifica que el servicio esté disponible al momento de reservar."""
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__servicio.nombre_servicio}' ({self.__servicio.id_entidad}) no está disponible."
            )
        return True

    def confirmar(self) -> None:
        """Cambia el estado de la reserva a CONFIRMADA si se encuentra PENDIENTE."""
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva '{self.id_entidad}' porque ya fue CANCELADA."
            )
        if self.__estado in ("CONFIRMADA", "PROCESADA"):
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id_entidad}' ya se encuentra en estado '{self.__estado}'."
            )
        # Revalida disponibilidad antes de confirmar
        self.validar()
        self.__estado = "CONFIRMADA"

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:
        """Cancela la reserva siempre que no haya sido ya procesada/facturada o cancelada."""
        if self.__estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"No es posible cancelar la reserva '{self.id_entidad}' porque ya fue PROCESADA."
            )
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id_entidad}' ya estaba cancelada previamente."
            )
        self.__estado = "CANCELADA"

    def procesar_reserva(
        self,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_extra: float = 0.0,
    ) -> float:
        """
        Procesa y liquida el costo de la reserva invocando polimórficamente el método
        sobrecargado calcular_costo del servicio asociado. Implementa encadenamiento de excepciones.
        """
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id_entidad}' debe estar CONFIRMADA antes de procesarse (estado actual: {self.__estado})."
            )
        try:
            # Llamada polimórfica al método sobrecargado calcular_costo
            total = self.__servicio.calcular_costo(
                duracion_horas=self.__duracion_horas,
                impuesto=impuesto,
                descuento=descuento,
                cargo_extra=cargo_extra,
            )
            self.__costo_final = total
            self.__estado = "PROCESADA"
            return self.__costo_final
        except CalculoInconsistenteError as exc:
            # Encadenamiento explícito: conserva la excepción matemática original y la eleva como error de reserva
            raise ReservaInvalidaError(
                f"Fallo al procesar liquidación de la reserva '{self.id_entidad}': {exc}"
            ) from exc

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre_servicio} | Duración: {self.__duracion_horas}h | "
            f"Estado: {self.__estado} | Total: ${self.__costo_final:,.2f}"
        )
