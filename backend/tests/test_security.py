import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient


class SecurityBaselineTests(unittest.TestCase):
    def test_invalid_bbox_is_rejected(self):
        from app.main import app

        with TestClient(app) as client:
            response = client.get("/cameras?bbox=invalid")

        self.assertEqual(response.status_code, 400)
        self.assertIn("bbox", response.json()["detail"])

    def test_admin_cache_endpoint_requires_key_in_production(self):
        with patch.dict(
            os.environ,
            {"APP_ENV": "production", "ADMIN_API_KEY": "test-admin-key"},
            clear=False,
        ):
            from app.config import get_settings

            get_settings.cache_clear()
            from app.main import app

            with TestClient(app) as client:
                response = client.delete("/satellite/cache")

            self.assertEqual(response.status_code, 401)
            get_settings.cache_clear()


if __name__ == "__main__":
    unittest.main()
