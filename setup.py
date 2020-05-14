#!/usr/bin/env python3

"""Python setup."""
import os
import re
from setuptools import setup


def read(file_name):
    """Return the contents of a file as a string."""
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as file:
        filestring = file.read()
    return filestring


def get_version():
    """Return the version of this module."""
    raw_init_file = read("kismet_rest/__init__.py")
    rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver


def build_long_desc():
    """Return the long description."""
    return "\n".join([read(f) for f in ["README.rst", "CHANGELOG.rst"]])


setup(name="kismet_rest",
      version=get_version(),
      author="Mike Kershaw / Dragorn",
      author_email="dragorn@kismetwireless.net",
      description="Simplified Python API for the Kismet REST interface",
      license="GPLv2",
      keywords="kismet",
      url="https://www.kismetwireless.net",
      download_url="https://kismetwireless.net/python-kismet-rest",
      packages=["kismet_rest"],
      install_requires="requests",
      long_description=build_long_desc(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Security",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
      ])
