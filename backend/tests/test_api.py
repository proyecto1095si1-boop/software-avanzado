import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_invalid_camera_bbox_is_rejected(self):
        response = self.client.get("/cameras", params={"bbox": "bad"})
        self.assertEqual(response.status_code, 422)
        self.assertIn("bbox", response.json()["detail"])

    def test_camera_bbox_returns_filtered_results(self):
        response = self.client.get("/cameras", params={"bbox": "-59,-35,-58,-34"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Buenos Aires - Obelisco", [cam["name"] for cam in response.json()["cameras"]])

    def test_cors_does_not_allow_arbitrary_origin(self):
        response = self.client.options(
            "/health",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertNotIn("access-control-allow-origin", response.headers)


if __name__ == "__main__":
    unittest.main()
