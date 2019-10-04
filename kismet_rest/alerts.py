"""Alerts abstraction."""

from .base_interface import BaseInterface


class Alerts(BaseInterface):
    """Alerts abstraction."""

    kwargs_defaults = {"ts_sec": 0, "ts_usec": 0}
    url_template = "alerts/last-time/{ts_sec}.{ts_usec}/alerts.itjson"

    def all(self, callback=None, callback_args=None, **kwargs):
        """Yield all alerts, one at a time.

        If callback is set, nothing will be returned.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Keyword args:
            ts_sec (int): Starting timestamp in seconds since Epoch.
            ts_usec (int): Microseconds for starting timestamp.

        Yield:
            dict: Alert json, or None if callback is set.
        """
        callback_settings = {}
        if callback:
            callback_settings["callback"] = callback
            if callback_args:
                callback_settings["callback_args"] = callback_args
        query_args = self.kwargs_defaults.copy()
        query_args.update(kwargs)
        url = self.url_template.format(**query_args)
        for result in self.interact_yield("GET", url, **callback_settings):
            yield result

    def define(self, name, description, rate="10/min", burst="1/sec",
               phyname=None):
        """Define an alert.

        LOGIN REQUIRED

        Define a new alert.  This alert can then be triggered on external
        conditions via raise_alert(...)

        Phyname is optional, and links the alert to a specific PHY type.

        Rate and Burst are optional rate and burst limits.

        Args:
            name (str): Name of alert.
            description (str): Description of alert.
            rate (str): Rate limit. Defaults to ``10/min``.
            burst (str): Burst limit. Defaults to ``1/sec``.
            phyname (str): Name of PHY. Defaults to None.

        Return:
            bool: True for success, False for failed request.
        """
        cmd = {"name": name,
               "description": description,
               "throttle": rate,
               "burst": burst}
        if phyname is not None:
            cmd["phyname"] = phyname
        url = "alerts/definitions/define_alert.cmd"
        return self.interact("POST", url, payload=cmd, only_status=True)

    def raise_alert(self, name, text, bssid=None, source=None, dest=None,
                    other=None, channel=None):
        """Raise an alert in Kismet.

        Trigger an alert; the alert can be one defined via define_alert(...) or
        an alert built into the system.

        The alert name and content of the alert are required, all other fields
        are optional.

        Args:
            name (str): Name of alert.
            text (str): Descriptive text for alert.
            bssid (str): BSSID to filter for.
            source (str): ...
            dest (str): ...
            other (str): ...
            channel (str): Channel to filter for.
        """

        cmd = {"name": name,
               "text": text}
        if bssid is not None:
            cmd["bssid"] = bssid
        if source is not None:
            cmd["source"] = source
        if dest is not None:
            cmd["dest"] = dest
        if other is not None:
            cmd["other"] = other
        if channel is not None:
            cmd["channel"] = channel
        return self.interact("POST", "alerts/raise_alert.cmd", payload=cmd,
                             only_status=True)
