****************
Mopidy-Bassdrive
****************

.. image:: https://pypip.in/v/Mopidy-Bassdrive/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-Bassdrive/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-Bassdrive/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-Bassdrive/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/felixb/mopidy-bassdrive.png?branch=development
    :target: https://travis-ci.org/felixb/mopidy-bassdrive
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/felixb/mopidy-bassdrive/badge.png?branch=development
   :target: https://coveralls.io/r/felixb/mopidy-bassdrive?branch=development
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Bassdrive <http://bassdrive.com>`_, archives and stream.


Installation
============

Install the Mopidy-Bassdrive extension by running::

    pip install mopidy-bassdrive


Configuration
=============

This is the default config of mopidy-bassdrive::

    [bassdrive]
    # enable plugin
    enabled = true
    # cache archive for 24h / 1140min
    refresh_archive = 1440


Usage
=====

The extension is enabled by default if all dependencies are
available. You can simply browse through the bassdrive archive or launch the
stream.


Project resources
=================

- `Source code <https://github.com/felixb/mopidy-Bassdrive>`_
- `Issue tracker <https://github.com/felixb/mopidy-Bassdrive/issues>`_
- `Download development snapshot
  <https://github.com/felixb/mopidy-Bassdrive/archive/develop.zip>`_


Changelog
=========

v0.1 (2014-07-29)
-----------------

- Cache archive structure

v0.0.1 (2014-07-28)
-------------------

- Initial release
