from __future__ import unicode_literals

import logging
import urllib

from bs4 import BeautifulSoup

from mopidy import backend
from mopidy.models import Ref

logger = logging.getLogger(__name__)


class BassdriveLibraryProvider(backend.LibraryProvider):
    root_url = 'http://archives.bassdrivearchive.com'
    stream_url = 'http://bassdrive.com/v2/streams/BassDrive.pls'
    root_directory = Ref.directory(uri='bassdrive:archive',
                                   name='Bassdrive Archive')

    def __init__(self, *args, **kwargs):
        super(BassdriveLibraryProvider, self).__init__(*args, **kwargs)

    def browse(self, uri):
        logger.info('browse: %s', str(uri))
        if not uri:
            return []

        # show root
        if uri == 'bassdrive:archive':
            # add current stream
            refs = [Ref.track(uri=BassdriveLibraryProvider.stream_url,
                              name='Bassdrive stream')]
            # browse archive
            fd = urllib.urlopen(BassdriveLibraryProvider.root_url)
            soup = BeautifulSoup(fd)
            container = soup.find(id='listingContainer')
            if container:
                for link in soup.find_all('a'):
                    url = link.get('href', None)
                    name = link.string
                    if url and name:
                        refs.append(Ref.album(uri='bassdrive:archive:%s' % url,
                                              name=name))
                return refs

        parts = uri.split(':')

        # browse archive
        # uri == 'bassdrive:archive:/url
        if len(parts) == 3 and parts[1] == 'archive':
            base_url = parts[2]
            fd = urllib.urlopen(
                'http://archives.bassdrivearchive.com%s' % base_url)
            soup = BeautifulSoup(fd)
            refs = []
            for link in soup.find_all('a'):
                url = link.get('href', None)
                name = link.string
                if url and name and str(url[0]) != '/':
                    name = str(name).strip()
                    url = base_url + url
                    logger.info('URL: %r', url)
                    if url[-1] == '/':
                        refs.append(Ref.album(uri='bassdrive:archive:%s' % url,
                                              name=name))
                    else:
                        refs.append(Ref.track(
                            uri=BassdriveLibraryProvider.root_url + url,
                            name=name))
            return refs

        logger.warning('Unknown uri: %r', uri)
        return []

    def lookup(self, uri):
        # TODO
        return []

    def refresh(self, uri=None):
        # nothing to do
        pass

    def search(self, query=None, uris=None):
        # TODO
        return []
