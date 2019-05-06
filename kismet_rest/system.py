"""Abstraction for system endpoint."""
import datetime

from .base_interface import BaseInterface


class System(BaseInterface):
    """Wrap all interaction with /system/ endpoint."""

    def get_status(self):
        """Return json representing Kismet system status."""
        return self.interact("GET", "system/status.json")

    def get_system_time(self, time_format=None):
        """Return current time from Kismet REST API.

        Args:
            format (str or None): Format time before returning. Supported
                formats: None (return as dict), ``iso`` (ISO 8601). Defaults
                to None.
        """
        from_api = self.interact("GET", "system/timestamp.json")
        if time_format is None:
            return from_api
        if time_format == "iso":
            seconds = from_api["kismet.system.timestamp.sec"]
            u_seconds = from_api["kismet.system.timestamp.usec"]
            timestamp = float(float(seconds) + (u_seconds / 1000000.0))
            return datetime.datetime.fromtimestamp(timestamp).isoformat()
        raise ValueError("Invalid system time format: {}".format(format))
