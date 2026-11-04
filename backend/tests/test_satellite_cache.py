import asyncio
import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

from app.satellite import cache


class SatelliteCacheTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await cache.clear_cache()

    async def asyncTearDown(self):
        await cache.clear_cache()

    async def test_cached_entry_expires_using_configured_ttl(self):
        now = datetime.now(timezone.utc)
        cache._cache["stations"] = (now - timedelta(seconds=11), [{"name": "ISS"}])

        with patch.object(cache, "get_settings", return_value=SimpleNamespace(tle_cache_ttl_seconds=10)):
            result = await cache.get_cached("stations")

        self.assertIsNone(result)
        self.assertNotIn("stations", cache._cache)

    async def test_entry_is_available_before_configured_ttl(self):
        satellites = [{"name": "ISS"}]
        cache._cache["stations"] = (datetime.now(timezone.utc), satellites)

        with patch.object(cache, "get_settings", return_value=SimpleNamespace(tle_cache_ttl_seconds=60)):
            result = await cache.get_cached("stations")

        self.assertEqual(result, satellites)

    def test_cache_stats_use_configured_ttl(self):
        cache._cache["stations"] = (
            datetime.now(timezone.utc) - timedelta(seconds=3),
            [{"name": "ISS"}],
        )

        with patch.object(cache, "get_settings", return_value=SimpleNamespace(tle_cache_ttl_seconds=10)):
            stats = cache.cache_stats()

        self.assertEqual(stats["stations"]["count"], 1)
        self.assertGreaterEqual(stats["stations"]["expires_in_seconds"], 6)
        self.assertLessEqual(stats["stations"]["expires_in_seconds"], 7)

    async def test_zero_or_negative_ttl_expires_immediately(self):
        await cache.set_cached("stations", [{"name": "ISS"}])

        with patch.object(cache, "get_settings", return_value=SimpleNamespace(tle_cache_ttl_seconds=-1)):
            result = await cache.get_cached("stations")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
