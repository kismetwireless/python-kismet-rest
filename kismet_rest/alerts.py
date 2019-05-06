"""Alerts abstraction."""

from .base_interface import BaseInterface


class Alerts(BaseInterface):
    """Alerts abstraction."""

    kwargs_defaults = {"ts_sec": 0, "ts_usec": 0}
    url_template = "alerts/last-time/{ts_sec}.{ts_usec}/alerts.ekjson"

    def yield_all(self, callback=None, callback_args=None, **kwargs):
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
        print(kwargs)
        print(query_args)
        query_args.update(kwargs)
        print(query_args)
        url = self.url_template.format(**query_args)
        for result in self.interact_yield("GET", url, **callback_settings):
            yield result
