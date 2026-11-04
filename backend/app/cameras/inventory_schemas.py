"""Esquemas para inventario administrado de cámaras autorizadas.

El esquema valida datos de entrada; no realiza descubrimiento ni conexiones.
"""

import re
from enum import Enum
from ipaddress import ip_address

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CameraManagementProtocol(str, Enum):
    ONVIF_HTTPS = "onvif_https"
    VENDOR_HTTPS_API = "vendor_https_api"
    VMS_API = "vms_api"


class CameraEnrollmentRequest(BaseModel):
    """Datos mínimos de inventario aportados por un operador autorizado."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    site_id: str = Field(min_length=1, max_length=100)
    network_scope_id: str = Field(
        min_length=1,
        max_length=100,
        description="Identificador de un alcance de red que el administrador aprobó por separado.",
    )
    address: str = Field(
        min_length=1,
        max_length=253,
        description="IP o hostname registrado; no admite esquema, ruta, query ni credenciales.",
    )
    port: int = Field(default=443, ge=1, le=65535)
    management_protocol: CameraManagementProtocol
    authorization_reference: str = Field(
        min_length=1,
        max_length=200,
        description="Referencia a la autorización o inventario del propietario; nunca un secreto.",
    )

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str) -> str:
        value = value.strip()
        if not value or any(char in value for char in "/?#@"):
            raise ValueError("Debe ser una IP o hostname, no una URL ni una credencial")
        try:
            return str(ip_address(value))
        except ValueError:
            if not value.isascii() or len(value) > 253:
                raise ValueError("Hostname inválido") from None
            hostname = value[:-1] if value.endswith(".") else value
            labels = hostname.split(".")
            label_pattern = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
            if not hostname or any(not label_pattern.fullmatch(label) for label in labels):
                raise ValueError("Debe ser una IP o hostname válido")
            return hostname.lower()
