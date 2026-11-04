import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.integrations.contracts import SourceState
from app.integrations.providers.space.celestrak import CelesTrakConnector


class CelesTrakConnectorTests(unittest.IsolatedAsyncioTestCase):
    async def test_healthy_when_tle_present(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "ISS (ZARYA)\n"
            "1 25544U 98067A   26001.50000000  .00000000  00000-0  00000-0 0  9990\n"
            "2 25544  51.6400 000.0000 0000001 000.0000 000.0000 15.50000000000000\n"
        )
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response

        with patch("app.integrations.providers.space.celestrak.httpx.AsyncClient", return_value=mock_client):
            connector = CelesTrakConnector()
            health = await connector.health_check()

        self.assertEqual(health.connector_id, "celestrak")
        self.assertEqual(health.state, SourceState.HEALTHY)
        self.assertIsNotNone(health.last_success_at)

    async def test_degraded_when_no_tle_format(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<!DOCTYPE html><html>not tle</html>"
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response

        with patch("app.integrations.providers.space.celestrak.httpx.AsyncClient", return_value=mock_client):
            connector = CelesTrakConnector()
            health = await connector.health_check()

        self.assertEqual(health.state, SourceState.DEGRADED)

    async def test_unavailable_on_http_error(self):
        import httpx

        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=mock_response
        )

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response

        with patch("app.integrations.providers.space.celestrak.httpx.AsyncClient", return_value=mock_client):
            connector = CelesTrakConnector()
            health = await connector.health_check()

        self.assertEqual(health.state, SourceState.UNAVAILABLE)
        self.assertIn("503", health.message or "")


if __name__ == "__main__":
    unittest.main()
