"""Adaptadores de datos espaciales autorizados.

CelesTrakConnector es el único adaptador activo de este paquete.
Los demás (Space-Track, N2YO, telemetría de misión) permanecen como
scaffolds hasta que exista autorización y configuración explícita.
"""

from app.integrations.providers.space.celestrak import CelesTrakConnector

__all__ = ["CelesTrakConnector"]
