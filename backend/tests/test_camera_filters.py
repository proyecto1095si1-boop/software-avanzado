import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.cameras.service import list_cameras


class CameraBoundingBoxTests(unittest.TestCase):
    def test_rejects_malformed_bbox(self):
        with self.assertRaisesRegex(ValueError, "cuatro coordenadas"):
            list_cameras(bbox="-70,-40,not-a-number,-30")

    def test_rejects_out_of_range_latitude(self):
        with self.assertRaisesRegex(ValueError, "latitudes"):
            list_cameras(bbox="-70,-100,-60,-30")

    def test_rejects_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "finitas"):
            list_cameras(bbox="-70,-40,inf,-30")

    def test_accepts_bbox_crossing_antimeridian(self):
        fixtures = [
            SimpleNamespace(id="east", name="east", longitude=179, latitude=0),
            SimpleNamespace(id="west", name="west", longitude=-179, latitude=0),
            SimpleNamespace(id="inside", name="inside", longitude=0, latitude=0),
        ]
        with patch("app.cameras.service.get_all_cameras", return_value=fixtures):
            cameras = list_cameras(bbox="170,-90,-170,90")
        self.assertEqual([camera.id for camera in cameras], ["east", "west"])

    def test_regular_bbox_still_filters_known_camera(self):
        cameras = list_cameras(bbox="-59,-35,-58,-34")
        self.assertIn("Buenos Aires - Obelisco", [camera.name for camera in cameras])


if __name__ == "__main__":
    unittest.main()
