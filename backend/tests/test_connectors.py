import unittest
from datetime import datetime, timezone

from pydantic import ValidationError

from app.integrations.contracts import ConnectorHealth, DataEnvelope, DataKind, SourceState
from app.integrations.registry import ConnectorRegistry


class FakeConnector:
    def __init__(self, connector_id, *, error=None, reported_id=None):
        self.connector_id = connector_id
        self.error = error
        self.reported_id = reported_id or connector_id

    async def health_check(self):
        if self.error:
            raise RuntimeError(self.error)
        return ConnectorHealth(
            connector_id=self.reported_id,
            state=SourceState.HEALTHY,
        )


class ConnectorRegistryTests(unittest.IsolatedAsyncioTestCase):
    def test_registers_and_lists_explicit_connectors(self):
        registry = ConnectorRegistry()
        registry.register(FakeConnector("zeta"))
        registry.register(FakeConnector("alpha"))
        self.assertEqual(registry.list_ids(), ["alpha", "zeta"])
        self.assertIsNotNone(registry.get("alpha"))
        self.assertIsNone(registry.get("missing"))

    def test_rejects_duplicate_connector_ids(self):
        registry = ConnectorRegistry()
        registry.register(FakeConnector("feed"))
        with self.assertRaisesRegex(ValueError, "ya está registrado"):
            registry.register(FakeConnector("feed"))

    async def test_connector_failure_is_isolated_and_redacted(self):
        registry = ConnectorRegistry()
        registry.register(FakeConnector("broken", error="secret-token=do-not-leak"))
        results = await registry.check_all()
        self.assertEqual(results[0].state, SourceState.UNAVAILABLE)
        self.assertNotIn("secret-token", results[0].message)

    async def test_mismatched_health_id_is_degraded(self):
        registry = ConnectorRegistry()
        registry.register(FakeConnector("feed", reported_id="other"))
        results = await registry.check_all()
        self.assertEqual(results[0].connector_id, "feed")
        self.assertEqual(results[0].state, SourceState.DEGRADED)

    def test_data_envelope_preserves_provenance_and_kind(self):
        envelope = DataEnvelope[dict](
            source_id="demo-feed",
            observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            kind=DataKind.OBSERVED,
            quality=0.9,
            payload={"value": 42},
        )
        self.assertEqual(envelope.source_id, "demo-feed")
        self.assertEqual(envelope.kind, DataKind.OBSERVED)
        self.assertIsNotNone(envelope.ingested_at)


if __name__ == "__main__":
    unittest.main()
