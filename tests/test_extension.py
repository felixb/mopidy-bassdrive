import unittest

import mock

from mopidy_bassdrive import BassdriveExtension, actor as backend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = BassdriveExtension()

        config = ext.get_default_config()

        self.assertIn('[bassdrive]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = BassdriveExtension()
        schema = ext.get_config_schema()
        self.assertIsNotNone(schema)

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = BassdriveExtension()
        ext.setup(registry)

        registry.add.assert_called_once_with(
            'backend', backend_lib.BassdriveBackend)

    def test_init_backend(self):
        ext = BassdriveExtension()
        backend = backend_lib.BassdriveBackend(ext, None)
        backend.on_start()

    def test_browse(self):
        ext = BassdriveExtension()
        backend = backend_lib.BassdriveBackend(ext, None)
        res = backend.library.browse(None)
        self.assertEqual(res, [])
        res = backend.library.browse('foo')
        self.assertEqual(res, [])
        res = backend.library.browse('bassdrive:archive')
        self.assertTrue(len(res) > 0)
        res = backend.library.browse('bassdrive:archive:/1%20-%20Monday/')
        self.assertTrue(len(res) > 0)
        res = backend.library.browse(
            'bassdrive:archive:' +
            '/1%20-%20Monday/The%20Technimatic%20Show%20-%20Technimatic/')
        self.assertTrue(len(res) > 0)

    def test_lookup(self):
        ext = BassdriveExtension()
        backend = backend_lib.BassdriveBackend(ext, None)
        res = backend.library.lookup(None)
        self.assertEqual(res, [])
        res = backend.library.lookup('bassdrive:archive')
        self.assertEqual(res, [])

    def test_search(self):
        ext = BassdriveExtension()
        backend = backend_lib.BassdriveBackend(ext, None)
        res = backend.library.search()
        self.assertEqual(res, [])
