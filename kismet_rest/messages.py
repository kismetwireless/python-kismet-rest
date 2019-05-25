"""Messages abstraction."""

from .base_interface import BaseInterface


class Messages(BaseInterface):
    """Messages abstraction."""

    kwargs_defaults = {"ts_sec": 0, "ts_usec": 0}
    url_template = "messagebus/last-time/{ts_sec}.{ts_usec}/messages.json"

    def all(self, callback=None, callback_args=None, **kwargs):
        """Yield all messages, one at a time.

        If callback is set, nothing will be returned.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Keyword args:
            ts_sec (int): Seconds since epoch for first message retrieved.
            ts_usec (int): Microseconds modifier for ts_sec query argument.

        Yield:
            dict: Message json, or None if callback is set.
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
