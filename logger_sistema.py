"""
Módulo: logger_sistema.py
Descripción: Configura el sistema de registro de eventos y errores en archivo plano
(registro_sistema.log), garantizando trazabilidad sin usar bases de datos.
"""

import logging
import os


def configurar_logger(ruta_archivo: str = "registro_sistema.log") -> logging.Logger:
    """
    Inicializa y configura el registrador (logger) institucional de Software FJ.
    
    Parámetros:
        ruta_archivo (str): Nombre o ruta del archivo de texto donde se guardarán los logs.
    Retorna:
        logging.Logger: Instancia configurada lista para registrar eventos y excepciones.
    """
    # Se obtiene o crea una instancia de logger con nombre único para el sistema
    logger = logging.getLogger("SoftwareFJ_Logger")
    logger.setLevel(logging.DEBUG)

    # Evita duplicar manejadores (handlers) si la función es llamada múltiples veces
    if not logger.handlers:
        # Formato detallado con marca de tiempo, nivel de severidad, módulo y mensaje
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Manejador de archivo en modo escritura ('w' para cada simulación limpia o 'a' para historial)
        manejador_archivo = logging.FileHandler(ruta_archivo, mode="w", encoding="utf-8")
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)

        # Se vincula el manejador de archivo al logger principal
        logger.addHandler(manejador_archivo)

    return logger
