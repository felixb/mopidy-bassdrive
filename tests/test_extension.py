import unittest

import mock

from mopidy_bassdrive import BassdriveExtension, actor as backend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = BassdriveExtension()

        config = ext.get_default_config()

        self.assertIn('[bassdrive]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('refresh_archive = 1440', config)

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
