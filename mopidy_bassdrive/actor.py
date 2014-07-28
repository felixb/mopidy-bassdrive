from __future__ import unicode_literals

from mopidy import backend

import pykka

from .library import BassdriveLibraryProvider


class BassdriveBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(BassdriveBackend, self).__init__()

        self.config = config

        self.library = BassdriveLibraryProvider(backend=self)

        self.uri_schemes = ['bassdrive']

    def on_start(self):
        self.library.refresh()
        self.playlists.refresh()
