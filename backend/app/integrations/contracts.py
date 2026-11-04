"""Contratos compartidos para integraciones de datos externas.

Este módulo define tipos, no realiza tráfico de red. Los conectores concretos
se activarán solo cuando exista configuración, alcance autorizado y controles.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, Protocol, TypeVar

from pydantic import BaseModel, ConfigDict, Field


PayloadT = TypeVar("PayloadT")


class DataKind(str, Enum):
    OBSERVED = "observed"
    CALCULATED = "calculated"
    INFERRED = "inferred"


class SourceState(str, Enum):
    NOT_CONFIGURED = "not_configured"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class DataEnvelope(BaseModel, Generic[PayloadT]):
    """Dato normalizado con procedencia y tiempos explícitos."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1, max_length=100)
    observed_at: datetime
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    kind: DataKind
    quality: float | None = Field(default=None, ge=0.0, le=1.0)
    authorization_reference: str | None = Field(default=None, max_length=200)
    payload: PayloadT


class ConnectorHealth(BaseModel):
    """Estado público y redactado de un conector."""

    model_config = ConfigDict(extra="forbid")

    connector_id: str = Field(min_length=1, max_length=100)
    state: SourceState
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_success_at: datetime | None = None
    message: str | None = Field(default=None, max_length=240)


class Connector(Protocol):
    """Interfaz mínima que deben implementar conectores concretos."""

    @property
    def connector_id(self) -> str: ...

    async def health_check(self) -> ConnectorHealth: ...


class SourceDescriptor(BaseModel):
    """Metadatos de catálogo, sin secretos ni configuración sensible."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1, max_length=100)
    display_name: str = Field(min_length=1, max_length=120)
    enabled: bool = False
    authorization_reference: str | None = Field(default=None, max_length=200)
    state: SourceState = SourceState.NOT_CONFIGURED
    data_kinds: list[DataKind] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
