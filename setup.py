#!/usr/bin/python

""" python setup file """

from setuptools import setup, find_packages

setup(name="Compta",
      version='0.0.1',
      description=open("README.md").read(),
      license="Copyright (C) 2015 David Micallef - All rights reserved",
      package_dir={'': 'lib'},
      packages=find_packages('lib'),
      download_url="http://www.micallef.fr/compta",
      url="http://www.micallef.fr/compta",
      author='David Micallef',
      author_email='david@micallef.fr',
      platforms=['GNU/Linux'],
      entry_points={
          "console_scripts": [
              "ComptaServer = compta.server.server:main",
              "ComptaCli = compta.cli.server:main"
              ]
          },
      classifiers=[
          "Environment :: Console",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Database :: Database Engines/Servers",
          "Development Status :: 1 - Alpha",
          "Framework :: Bottle",
          ],
      )
