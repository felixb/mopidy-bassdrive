from __future__ import unicode_literals

import os

from mopidy import config, ext


__version__ = '0.1'


class BassdriveExtension(ext.Extension):

    dist_name = 'Mopidy-Bassdrive'
    ext_name = 'bassdrive'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(BassdriveExtension, self).get_config_schema()
        schema['refresh_archive'] = config.Integer(minimum=0, optional=True)
        return schema

    def setup(self, registry):
        from .actor import BassdriveBackend
        registry.add('backend', BassdriveBackend)
