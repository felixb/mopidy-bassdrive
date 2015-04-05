from __future__ import unicode_literals

import logging
import re
import urllib

from bs4 import BeautifulSoup

from mopidy import backend
from mopidy.models import Album, Artist, Ref, Track

logger = logging.getLogger(__name__)


class BassdriveLibraryProvider(backend.LibraryProvider):
    _genre = 'Drum and Bass'
    _pattern = re.compile('/[^/]*/([^-]*)-([^/]*)/' +
                          '\[(\d\d\d\d)\.(\d\d)\.(\d\d)\] (.*)\.mp3')
    _archive_uri_base = 'bassdrive:archive'
    _archive_uri = 'bassdrive:archive:%s'
    _archive_url = 'http://archives.bassdrivearchive.com'
    _stream_uri = 'bassdrive:stream'
    _stream_url = 'http://bassdrive.com/v2/streams/BassDrive.pls'
    _stream_track = Track(
        uri=_stream_url,
        name='Bassdrive - Worldwide Drum and Bass Radio',
        genre=_genre
    )
    root_directory = Ref.directory(uri=_archive_uri_base,
                                   name='Bassdrive Archive')

    def __init__(self, *args, **kwargs):
        super(BassdriveLibraryProvider, self).__init__(*args, **kwargs)
        self._refs = {}
        self._albums = {}
        self._artists = {}
        self._tracks = {}

    def browse(self, uri):
        logger.debug('browse: %r', uri)
        if not uri:
            return []

        if uri in self._refs:
            return self._refs[uri]

        # show root
        if uri == self._archive_uri_base:
            # add current stream
            refs = [self._track_to_ref(self._stream_track, self._stream_uri)]
            # browse archive
            fd = urllib.urlopen(self._archive_url)
            soup = BeautifulSoup(fd)
            container = soup.find(id='listingContainer')
            if container:
                for link in soup.find_all('a'):
                    url = link.get('href', None)
                    name = link.string
                    if url and name and name[0] in '1234567':
                        # show active shows only
                        # former shows are down
                        # file names for special events/shows are hard to parse
                        refs.append(Ref.album(
                            uri=self._archive_uri % url,
                            name=name))
                if len(refs) > 0:
                    self._refs[uri] = refs
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
                name = str(link.string).strip('/')
                if url and name and str(url[0]) != '/':
                    name = str(name).strip()
                    url = base_url + url
                    ref_uri = self._archive_uri % url
                    logger.debug('ref_uri: %r', ref_uri)
                    if url[-1] == '/':
                        refs.append(Ref.album(
                            uri=ref_uri,
                            name=name))
                    else:
                        track = self._link_to_track(ref_uri)
                        if track:
                            refs.append(self._track_to_ref(track, ref_uri))
            if len(refs) > 0:
                self._refs[uri] = refs
            return refs

        logger.warning('Unknown uri: %r', uri)
        return []

    def lookup(self, uri):
        logger.debug('lookup: %r', uri)
        if not uri:
            return []
        if uri == self._stream_uri:
            return [self._stream_track]
        if uri.startswith(self._archive_uri % '/'):
            track = self._link_to_track(uri)
            if track:
                return [track]
        logger.warning('Lookup failed for unknown uri: %r', uri)
        return []

    def refresh(self, uri=None):
        # flush cache
        self._refs = {}
        self._albums = {}
        self._artists = {}
        self._tracks = {}
        # prefetch bassdrive root
        self.browse('bassdrive:archive')

    # TODO Implement search()

    def _link_to_track(self, uri):
        if uri in self._tracks:
            return self._tracks[uri]

        link = uri.split(':')[2]
        link_u = urllib.unquote(link).decode('utf8')
        m = self._pattern.match(link_u)
        if not m:
            logger.warning('Unknown link format: %r', link)
            return None
        album_name = m.group(1).strip()
        artist_name = m.group(2).strip()
        year, month, day = m.group(3, 4, 5)
        title = '[%s-%s-%s] %s' % (year, month, day, album_name)
        artist_uri = 'bassdrive:artist:%s' % artist_name
        album_uri = 'bassdrive:artist:%s-%s' % (year, album_name)
        if artist_uri in self._artists:
            artist = self._artists[artist_uri]
        else:
            artist = Artist(uri=artist_uri,
                            name=artist_name)
            self._artists[artist_uri] = artist
        if album_uri in self._albums:
            album = self._albums[album_uri]
        else:
            album = Album(uri=album_uri,
                          name=album_name,
                          date=year,
                          artists=[artist])
            self._albums[album_uri] = album

        track = Track(
            uri=self._archive_url + link,
            name=title,
            album=album,
            artists=[artist],
            genre=self._genre,
            date=year
        )
        self._tracks[uri] = track
        return track

    # noinspection PyMethodMayBeStatic
    def _track_to_ref(self, track, uri=None):
        if not uri:
            uri = track.uri
        name = ''
        for artist in track.artists:
            if len(name) > 0:
                name += ', '
            name += artist.name
        if (len(name)) > 0:
            name += ' - '
        name += track.name
        return Ref.track(uri=uri, name=name)
