"""GPS abstraction."""

from .base_interface import BaseInterface


class GPS(BaseInterface):
    """GPS abstraction."""

    def current_location(self):
        """Return the gps location.

        Return:
            dict: Dictionary object describing current location of Kismet
                server. Keys represented in output:
                ``kismet.common.location.lat``,
                ``kismet.common.location.lon``,
                ``kismet.common.location.alt``,
                ``kismet.common.location.heading``,
                ``kismet.common.location.speed``,
                ``kismet.common.location.time_sec``,
                ``kismet.common.location.time_usec``,
                ``kismet.common.location.fix``,
                ``kismet.common.location.valid``
        """
        return self.interact("GET", "gps/location.json")
