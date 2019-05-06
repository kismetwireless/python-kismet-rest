"""General utility functions located here."""

import os
import re
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class Utility(object):
    """Utility class."""

    @classmethod
    def build_full_url(cls, base_url, url_path):
        """Return a complete, well-formed URL.

        Args:
            base_url (str): Protocol, FQDN, port, and optional base path for
                query. Base path is unnecessary unless Kismet is behind a
                proxy.
            url_path (str): Relative URL path to Kismet API endpoint.

        Returns:
            str: Complete URL.

        """
        base = "{}/".format(base_url.rstrip("/"))  # Must always be one "/"
        result = urljoin(base, url_path.lstrip("/"))
        return result

    @classmethod
    def get_lib_version(cls):
        """Get version of kismet_Rest library."""
        here_dir = os.path.abspath(os.path.dirname(__file__))
        initfile = os.path.join(here_dir, "__init__.py")
        raw_init_file = cls.readfile(initfile)
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        ver = rx_compiled.search(raw_init_file).group(1)
        return ver

    @classmethod
    def readfile(cls, file_name):
        """Return contents of a file as a string."""
        with open(file_name, 'r') as file:
            filestring = file.read()
        return filestring
