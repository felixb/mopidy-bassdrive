import time

import unittest

from mopidy_bassdrive import BassdriveExtension, actor as backend_lib


class BackendTest(unittest.TestCase):

    def _get_config(self, ext):
        config = ext.get_config_schema()
        config['refresh_archive'] = 1440
        return {'bassdrive': config}

    def setUp(self):
        self.ext = BassdriveExtension()
        config = self._get_config(self.ext)
        self.backend = backend_lib.BassdriveBackend(config, None)

    def test_init_backend(self):
        self.backend.on_start()
        time.sleep(3)
        self.assertIsNotNone(self.backend._refresh_timer)
        self.backend.on_stop()
        self.assertIsNone(self.backend._refresh_timer)

    def test_init_backend_no_refresh(self):
        self.ext = BassdriveExtension()
        config = self._get_config(self.ext)
        config['bassdrive']['refresh_archive'] = 0
        self.backend = backend_lib.BassdriveBackend(config, None)
        self.backend.on_start()
        time.sleep(3)
        self.assertIsNone(self.backend._refresh_timer)
        self.backend.on_stop()
        self.assertIsNone(self.backend._refresh_timer)

    def test_browse(self):
        res = self.backend.library.browse(None)
        self.assertEqual(res, [])
        res = self.backend.library.browse('foo')
        self.assertEqual(res, [])
        res = self.backend.library.browse('bassdrive:archive')
        self.assertTrue(len(res) > 0)
        res = self.backend.library.browse('bassdrive:archive:/1%20-%20Monday/')
        self.assertTrue(len(res) > 0)
        res = self.backend.library.browse(
            'bassdrive:archive:' +
            '/1%20-%20Monday/The%20Technimatic%20Show%20-%20Technimatic/')
        self.assertTrue(len(res) > 0)

    def test_cache_init(self):
        self.backend.on_start()
        time.sleep(3)
        self.assertTrue(len(self.backend.library._cache) > 0)
        self.backend.on_stop()

    def test_cache(self):
        uri = 'bassdrive:archive:/1%20-%20Monday/'
        # cache is empty, because on_start() was not run
        self.assertTrue(len(self.backend.library._cache) == 0)
        res0 = self.backend.library.browse(uri)
        self.assertTrue(len(self.backend.library._cache) > 0)
        self.assertIn(uri, self.backend.library._cache)
        self.assertEqual(res0, self.backend.library._cache[uri])
        res1 = self.backend.library.browse(uri)
        self.assertEqual(res0, res1)

    def test_lookup(self):
        res = self.backend.library.lookup(None)
        self.assertEqual(res, [])
        res = self.backend.library.lookup('bassdrive:archive')
        self.assertEqual(res, [])

    def test_search(self):
        res = self.backend.library.search()
        self.assertEqual(res, [])
