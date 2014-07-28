from __future__ import unicode_literals

from threading import Timer

from mopidy import backend

import pykka

from .library import BassdriveLibraryProvider


class BassdriveBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(BassdriveBackend, self).__init__()

        self.config = config
        self._refresh_archive = self.config['bassdrive']['refresh_archive']
        self._refresh_timer = None

        self.library = BassdriveLibraryProvider(backend=self)

        self.uri_schemes = ['bassdrive']

    def on_start(self):
        self._schedule_refresh(0.5)

    def on_stop(self):
        self._terminate_refresh()

    def _refresh_content(self):
        self.library.refresh()
        # schedule next refresh
        if self._refresh_archive > 0:
            self._schedule_refresh(self._refresh_archive * 60.0)
        else:
            self._terminate_refresh()

    def _schedule_refresh(self, seconds):
        self._refresh_timer = Timer(seconds, self._refresh_content)
        self._refresh_timer.start()

    def _terminate_refresh(self):
        if self._refresh_timer:
            self._refresh_timer.cancel()
            self._refresh_timer = None
