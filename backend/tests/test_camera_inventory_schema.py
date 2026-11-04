import unittest

from pydantic import ValidationError

from app.cameras.inventory_schemas import CameraEnrollmentRequest, CameraManagementProtocol


def valid_payload(**overrides):
    payload = {
        "name": "Camera North Gate",
        "site_id": "site-01",
        "network_scope_id": "scope-campus-a",
        "address": "192.0.2.24",
        "port": 443,
        "management_protocol": CameraManagementProtocol.ONVIF_HTTPS,
        "authorization_reference": "asset-register-2026-001",
    }
    payload.update(overrides)
    return payload


class CameraEnrollmentSchemaTests(unittest.TestCase):
    def test_accepts_operator_registered_ip(self):
        camera = CameraEnrollmentRequest(**valid_payload())
        self.assertEqual(camera.address, "192.0.2.24")
        self.assertEqual(camera.port, 443)

    def test_normalizes_hostname(self):
        camera = CameraEnrollmentRequest(**valid_payload(address="Gate-Camera.Example"))
        self.assertEqual(camera.address, "gate-camera.example")

    def test_rejects_url_and_embedded_credentials(self):
        for address in (
            "https://camera.example/stream",
            "camera.example/path",
            "user:password@camera.example",
        ):
            with self.subTest(address=address):
                with self.assertRaises(ValidationError):
                    CameraEnrollmentRequest(**valid_payload(address=address))

    def test_rejects_secret_fields(self):
        with self.assertRaises(ValidationError):
            CameraEnrollmentRequest(**valid_payload(password="not-allowed"))

    def test_requires_site_scope_and_authorization_reference(self):
        for field in ("site_id", "network_scope_id", "authorization_reference"):
            with self.subTest(field=field):
                payload = valid_payload()
                payload.pop(field)
                with self.assertRaises(ValidationError):
                    CameraEnrollmentRequest(**payload)

    def test_rejects_invalid_port_and_host(self):
        for overrides in ({"port": 70000}, {"address": "bad host name"}):
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    CameraEnrollmentRequest(**valid_payload(**overrides))


if __name__ == "__main__":
    unittest.main()
