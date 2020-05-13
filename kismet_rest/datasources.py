"""Datasources abstraction."""

from .base_interface import BaseInterface


class Datasources(BaseInterface):
    """Datasources abstraction."""

    kwargs_defaults = {}
    url_template = "datasource/all_sources.itjson"

    def all(self, callback=None, callback_args=None):
        """Yield all datasources, one at a time.

        If callback is set, nothing will be returned.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Yield:
            dict: Datasource json, or None if callback is set.
        """
        callback_settings = {}
        if callback:
            callback_settings["callback"] = callback
            if callback_args:
                callback_settings["callback_args"] = callback_args
        url = self.url_template
        for result in self.interact_yield("GET", url, **callback_settings):
            yield result

    def interfaces(self, callback=None, callback_args=None):
        """Yield all interfaces, one at a time.

        If callback is set, nothing will be returned.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Yield:
            dict: Datasource json, or None if callback is set.
        """
        callback_settings = {}
        if callback:
            callback_settings["callback"] = callback
            if callback_args:
                callback_settings["callback_args"] = callback_args
        url = "datasource/list_interfaces.itjson"
        for result in self.interact_yield("GET", url, **callback_settings):
            yield result

    def set_channel(self, uuid, channel):
        """Return ``True`` if operation was successful, ``False`` otherwise.

        Locks an data source to an 802.11 channel or frequency.  Channel
        may be complex channel such as "6HT40+".

        Requires valid login.

        """
        cmd = {"channel": channel}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def set_hop_rate(self, uuid, rate):
        """Set the hop rate of a specific data source by UUID.

        Configures the hopping rate of a data source, while not changing the
        channels used for hopping.

        Requires valid login
        """
        cmd = {"rate": rate}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def set_hop_channels(self, uuid, rate, channels):
        """Set datasource hopping rate by UUID.

        Configures a data source for hopping at 'rate' over a vector of
        channels.

        Requires valid login
        """
        cmd = {"rate": rate,
               "channels": channels}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def set_hop(self, uuid):
        """Configure a source for hopping.

        Uses existing source hop / channel list / etc attributes.

        Requires valid login
        """
        cmd = {"hop": True}
        url = "datasource/by-uuid/{}/set_hop.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def add(self, source):
        """Add a new source to Kismet.

        source is a standard source definition.

        Requires valid login.

        Return:
            bool: Success
        """
        cmd = {"definition": source}
        return self.interact("POST", "datasource/add_source.cmd",
                             only_status=True, payload=cmd)

    def pause(self, source):
        """Pause source.

        Args:
            source (str): UUID of source to pause.

        Return:
            bool: Success

        """
        url = "/datasource/by-uuid/{}/pause_source.cmd".format(source)
        return self.interact("GET", url, only_status=True)

    def resume(self, source):
        """Resume paused source.

        Args:
            source (str): UUID of source to resume.

        Return:
            bool: Success

        """
        url = "/datasource/by-uuid/{}/resume_source.cmd".format(source)
        return self.interact("GET", url, only_status=True)

    def close(self, uuid):
        """Close source. A closed source will no longer be processed, and will remain closed unless reopened.

        Args:
            uuid (str): UUID of source to close.

        Return:
            bool: Success

        """
        url = "/datasource/by-uuid/{}/close_source.cmd".format(uuid)
        return self.interact("GET", url, only_status=True)

    def open(self, uuid):
        """Reopen a closed source.

        Args:
            uuid (str): UUID of source to open.

        Return:
            bool: Success

        """
        url = "/datasource/by-uuid/{}/open_source.cmd".format(uuid)
        return self.interact("GET", url, only_status=True)

