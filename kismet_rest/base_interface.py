"""Base interface. All API interaction, at a low level, happens here."""

import json
import os
import sys
from urllib3.util.retry import Retry

import requests
from requests.adapters import HTTPAdapter

from .logger import Logger
from .exceptions import KismetLoginException
from .exceptions import KismetRequestException
from .exceptions import KismetConnectionError
from .utility import Utility

if sys.version_info[0] < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

import base64

class BaseInterface(object):
    """Initialize with optional keyword arguments to override default settings.

    For compatibility with the original implementation, we support arguments
    and keyword arguments for host_uri and session_cache.

    Args:
        host_uri (str): URI for Kismet host. This setting is made available as
            an argument and a keyword argument. If both are set, the keyword
            argument takes precedence.
        session_cache (str): Path for storing session cache information. This
            setting is made available as an argument and a keyword argument.
            if the keyword argument is set, it takes precedence over the
            argument.
    Keyword Args:
        host_uri (str): URI for Kismet REST API. Defaults to
            ``http://127.0.0.1:2501``. If Kismet is behind a reverse proxy, add
            the base path to this url as well: ``https://my.proxy.com/kismet/``
        username (str): Username for administrative interaction with Kismet
            REST interface.
        password (str): Password corresponding to ``username``.
        session_cache (str): Path for storing session cache information.
            Defaults to `~/.pykismet_session`.
        debug (bool): Set to True to enble debug logging.
    """

    permitted_kwargs = ["host_uri", "username", "password",
                        "session_cache", "debug"]

    def __init__(self, host_uri='http://127.0.0.1:2501', **kwargs):
        """Initialize using legacy args or (new style) kwargs."""
        self.logger = Logger()
        self.max_retries = 5
        self.retry_statuses = [500]
        self.host_uri = host_uri
        self.username = None
        self.password = "nopass"
        self.sessioncache_path = '~/.pykismet_session_' + base64.b64encode(str.encode(host_uri)).decode("utf-8").strip("=")
        self.session_cache = self.sessioncache_path
        self.debug = False
        # Set the default path for storing sessions
        # self.sessioncache_path = None
        self.set_attributes_from_dict(kwargs)
        self.session = requests.Session()
        self.set_session_cache(self.session_cache)
        self.create_client()
        if self.debug:
            self.logger.set_debug()
        if self.username:
            self.set_login(self.username, self.password)
        self.is_py35 = sys.version_info[0] == 3 and sys.version_info[1] == 5

        try:
            self.login()
        except (requests.exceptions.ConnectionError) as err:
            msg = "Unable to connect to Kismet: {}".format(err)
            raise KismetConnectionError(msg)

    def set_attributes_from_dict(self, kwa):
        """Set instance attributes from dictionary if on whitelist."""
        for kwarg, val in kwa.items():
            if kwarg in self.permitted_kwargs:
                setattr(self, kwarg, val)

    def create_client(self):
        """Build client object for interaction with Kismet REST API.

        This client implements connection re-use and exponential back-off.
        """
        self.client = requests.Session()
        self.retries = Retry(total=self.max_retries,
                             status_forcelist=self.retry_statuses,
                             backoff_factor=1)
        self.http_adapter = HTTPAdapter(pool_connections=1,
                                        max_retries=self.retries)
        parsed_uri = urlparse(self.host_uri)
        proto = parsed_uri.scheme if parsed_uri.scheme else "http"
        host = parsed_uri.netloc
        self.session_mount = "{}://{}".format(proto, host)
        self.client.mount(self.session_mount, self.http_adapter)

    def log_init(self):
        """Initialize logging."""
        lib_ver = Utility.get_lib_version()
        kis_ver = self.get_kismet_version()
        msg = "Initialized kismetrest v{}, Kismet version {}".format(lib_ver,
                                                                     kis_ver)
        self.logger.debug(msg)

    def get_kismet_version(self):
        """Return version of Kismet, as reported by Kismet REST interface."""
        try:
            kismet_version = self.interact("GET", "system/status.json")
        except (requests.exceptions.ConnectionError) as err:
            msg = "Unable to connecto to Kismet: {}".format(err)
            raise KismetConnectionError(msg)
        return kismet_version

    def interact(self, verb, url_path, stream=False, **kwargs):
        """Wrap all low-level API interaction.

        Args:
            verb (str): ``GET`` or ``POST``.
            url_path (str): Path part of URL.
            stream (bool): Process as a stream, meaning that this function
                becomes a generator which yields results one at a time. This
                enables a lower memory footprint end-to-end, but requires a
                somewhat different approach to interacting with this function.

        Keyword Args:
            payload (dict): Dictionary with POST payload.
            only_status (bool): Only return boolean to represent success or
                failure of operation.
            callback (function): Callback to be used for each JSON object.
            callback_args (list): List of arguments for callback.

        Return:
            dict: JSON from API. String returned if return_string is set.
        """
        only_status = bool("only_status" in kwargs
                           and kwargs["only_status"] is True)
        payload = kwargs["payload"] if "payload" in kwargs else {}
        full_url = Utility.build_full_url(self.host_uri, url_path)
        if verb == "GET":
            self.logger.debug("interact: GET against {} "
                              "stream={}".format(full_url, stream))
            response = self.session.get(full_url, stream=stream)
        elif verb == "POST":
            if payload:
                postdata = json.dumps(payload)
            else:
                postdata = "{}"

            formatted_payload = {"json": postdata}
            self.logger.debug("interact: POST against {} "
                              "with {} stream={}".format(full_url,
                                                         formatted_payload,
                                                         stream))
            response = self.session.post(full_url, data=formatted_payload,
                                         stream=stream)

        else:
            self.logger.error("HTTP verb {} not yet supported!".format(verb))

        # Application error
        if response.status_code == 500:
            msg = "Kismet 500 Error response from {}: {}".format(url_path,
                                                                 response.text)
            self.logger.error(msg)
            raise KismetLoginException(msg, response.status_code)

        # Invalid request
        if response.status_code == 400:
            msg = "Kismet 400 Error response from {}: {}".format(url_path,
                                                                 response.text)
            self.logger.error(msg)
            raise KismetRequestException(msg, response.status_code)

        # login required
        if response.status_code == 401:
            msg = "Login required for {}".format(url_path)
            self.logger.error(msg)
            raise KismetLoginException(msg, response.status_code)

        # Did we succeed?
        if not response.status_code == 200:
            msg = "Request failed {} {}".format(url_path, response.status_code)
            self.logger.error(msg)
            raise KismetRequestException(msg, response.status_code)

        if only_status:
            return bool(response)  # We can test for good resp codes like this.
        if not stream:
            retval = self.process_response_bulk(response, **kwargs)
            self.update_session()
            return retval
        return [result for result in
                self.process_response_stream(response, **kwargs)]

    def interact_yield(self, verb, url_path, **kwargs):
        """Wrap all low-level API interaction.

        Args:
            verb (str): ``GET`` or ``POST``.
            url_path (str): Path part of URL.

        Keyword Args:
            payload (dict): Dictionary with POST payload.
            callback (function): Callback to be used for each JSON object.
            callback_args (list): List of arguments for callback.

        Yield:
            dict: JSON from API. String returned if return_string is set.
        """
        payload = kwargs["payload"] if "payload" in kwargs else {}
        full_url = Utility.build_full_url(self.host_uri, url_path)
        if verb == "GET":
            self.logger.debug("interact_yield: GET {}".format(full_url))
            response = self.session.get(full_url, stream=True)
        elif verb == "POST":
            if payload:
                postdata = json.dumps(payload)
            else:
                postdata = "{}"

            formatted_payload = {"json": postdata}
            self.logger.debug("interact_yield: POST against {} "
                              "with {}".format(full_url, formatted_payload))
            response = self.session.post(full_url, data=formatted_payload,
                                         stream=True)

        else:
            self.logger.error("HTTP verb {} not yet supported!".format(verb))

        # Application error
        if response.status_code == 500:
            msg = "Kismet 500 Error response from {}: {}".format(url_path,
                                                                 response.text)
            self.logger.error(msg)
            raise KismetLoginException(msg, response.status_code)

        # Invalid request
        if response.status_code == 400:
            msg = "Kismet 400 Error response from {}: {}".format(url_path,
                                                                 response.text)
            self.logger.error(msg)
            raise KismetRequestException(msg, response.status_code)

        # login required
        if response.status_code == 401:
            msg = "Login required for {}".format(url_path)
            self.logger.error(msg)
            raise KismetLoginException(msg, response.status_code)

        # Did we succeed?
        if not response.status_code == 200:
            msg = "Request failed {} {}".format(url_path, response.status_code)
            self.logger.error(msg)
            raise KismetRequestException(msg, response.status_code)
        for result in self.process_response_stream(response, **kwargs):
            yield result

    def process_response_stream(self, response, **kwargs):
        """Process API response as a stream."""
        response.encoding = 'utf-8'
        if "callback" in kwargs:
            callback_args = (kwargs["callback_args"]
                             if "callback_args" in kwargs
                             else [])
            for item in response.iter_lines(decode_unicode=True):
                if callback_args:
                    kwargs["callback"](json.loads(item), *callback_args)
                    continue
                kwargs["callback"](json.loads(item))
            return
        for result in response.iter_lines(decode_unicode=True):
            yield json.loads(result)

    def process_response_bulk(self, response, **kwargs):
        """Process API response as a single bulk interaction."""
        response.encoding = 'utf-8'
        if "callback" in kwargs:
            callback_args = (kwargs["callback_args"]
                             if "callback_args" in kwargs
                             else [])
            for item in response.json():
                if callback_args:
                    kwargs["callback"](item, *callback_args)
                    continue
                kwargs["callback"](item)
            return None
        return response.json()

    def set_session_cache(self, path):
        """Set a cache file for HTTP sessions.

        Args:
            path (str): Path to session cache file.

        """
        self.sessioncache_path = os.path.expanduser(path)
        # If we already have a session cache file here, load it
        if os.path.isfile(self.sessioncache_path):
            try:
                lcachef = open(self.sessioncache_path, "r")
                cookie = lcachef.read()
                # Add the session cookie
                requests.utils.add_dict_to_cookiejar(
                    self.session.cookies, {"KISMET": cookie})
                lcachef.close()
            except Exception as exc:
                if self.debug:
                    print("Failed to read session cache:", exc)

    def update_session(self):
        """Update the session key.

        Internal utility function for extracting an updated session key, if one
        is present, from the connection.  Typically called after fetching any
        URI.
        """
        try:
            c_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
            cookie = c_dict["KISMET"]
            if cookie:
                lcachef = open(self.sessioncache_path, "w")
                lcachef.write(cookie)
                lcachef.close()
        except KeyError:
            pass
        except Exception as exc:
            self.logger.error("DEBUG - Failed to save session: {}".format(exc))

    def set_login(self, username, password):
        """Set login credentials."""
        self.session.auth = (username, password)

    def set_debug(self):
        """Set debug mode for more verbose output."""
        self.logger.set_debug()

    def check_session(self):
        """Confirm session validity.

        Checks if a session is valid / session is logged in
        """
        response = self.session.get("%s/session/check_session" % self.host_uri)
        if not response.status_code == 200:
            return False
        self.update_session()
        return True

    def login(self):
        """Login to Kismet REST interface.

        Logs in (and caches login credentials).  Required for administrative
        behavior.
        """
        response = self.session.get("%s/session/check_session" % self.host_uri)
        if not response.status_code == 200:
            msg = "login(): Invalid session: {}".format(response.text)
            self.logger.debug(msg)
            return False
        self.update_session()
        return True
