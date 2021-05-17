"""Devices abstraction."""

from .base_interface import BaseInterface


class Devices(BaseInterface):
    """Devices abstraction."""

    kwargs_defaults = {"ts": 0}
    url_template = "devices/last-time/{ts}/devices.itjson"
    #url_template = "devices/views/all/last-time/{ts}/devices.itjson"

    def all(self, callback=None, callback_args=None, **kwargs):
        """Yield all devices, one at a time.

        If callback is set, nothing will be returned.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Keyword args:
            ts (int): Starting last-seen timestamp in seconds since Epoch.

        Yield:
            dict: Device json, or None if callback is set.
        """
        callback_settings = {}
        if callback:
            callback_settings["callback"] = callback
            if callback_args:
                callback_settings["callback_args"] = callback_args
        query_args = self.kwargs_defaults.copy()
        query_args.update(kwargs)
        url = self.url_template.format(**query_args)
        for result in self.interact_yield("POST", url, **callback_settings):
            yield result

    def by_mac(self, callback=None, callback_args=None, **kwargs):
        """Yield devices matching provided MAC addresses or masked MAC groups.

        Args:
            callback: Callback function.
            callback_args: Arguments for callback.

        Keyword args:
            devices (list): List of device MACs or MAC masks.
            fields (list): List of fields to return.

        Yield:
            dict: Device json, or None if callback is set.
        """
        call_settings = {}
        if callback:
            call_settings["callback"] = callback
            if callback_args:
                call_settings["callback_args"] = callback_args
        valid_kwargs = ["fields", "devices"]
        call_settings["payload"] = {kword: kwargs[kword]
                                    for kword in valid_kwargs
                                    if kword in kwargs}
        url = "devices/multimac/devices.itjson"
        for result in self.interact_yield("POST", url, **call_settings):
            yield result

    def by_key(self, device_key, field=None, fields=None):
        """Return a dictionary representing one device, identified by ``key``.

        Fetch a complete device record by the Kismet key (unique key per Kismet
        session) or fetch a specific sub-field by path.

        Return:
            dict: Dictionary object describing one device.
        """
        url = "devices/by-key/{}/device.json".format(device_key)
        if not fields and field:
            url = "{}/{}".format(url, field)
        elif fields:
            payload = {"fields": fields}
            return self.interact("POST", url, payload=payload)
        return self.interact("POST", url)

    def dot11_clients_of(self, ap_id, callback=None, callback_args=None,
                         **kwargs):
        """List clients of an 802.11 AP.

        List devices which are clients of a given 802.11 access point, using
        the /phy/phy80211/clients-of endpoint.

        Returned devices can be summarized/simplified by the fields list.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be yielded.

        Args:
            ap_id (str): ID of AP to return clients for. (kismet.device.base.key)
            callback: Callback function.
            callback_args: Arguments for callback.

        Yield:
            dict: Dictionary describing a client of the identified AP.
        """
        call_settings = {}
        if callback:
            call_settings["callback"] = callback
            if callback_args:
                call_settings["callback_args"] = callback_args
        valid_kwargs = ["fields"]
        call_settings["payload"] = {kword: kwargs[kword]
                                    for kword in valid_kwargs
                                    if kword in kwargs}
        url = "phy/phy80211/clients-of/{}/clients.itjson".format(ap_id)
        for result in self.interact_yield("POST", url, **call_settings):
            yield result

    def dot11_access_points(self, callback=None, callback_args=None, **kwargs):
        """Return a list of dot11 access points.

        List devices which are considered to be 802.11 access points, using the
        /devices/views/phydot11_accesspoints/ view

        Returned devices can be summarized/simplified by the fields list.

        If a timestamp is given, only devices modified more recently than the
        timestamp (and matching any other conditions) will be returned.

        If a regex is given, only devices matching the regex (and any other
        conditions) will be returned.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be yielded as
        dictionary objects.

        Args:
            callback (obj): Callback for processing individual results.
            cbargs (list): List of arguments for callback.

        Keyword args:
            last_time (int): Unix epoch timestamp
            regex (str): Regular expression for filtering results.
            fields (list): Fields for filtering.

        Yield:
            dict: Dictionary-type objects which describe access points.
                Keys describing access points:
                ``dot11.device``,
                ``kismet.device.base.basic_crypt_set``,
                ``kismet.device.base.basic_type_set``,
                ``kismet.device.base.channel``,
                ``kismet.device.base.commonname``,
                ``kismet.device.base.crypt``,
                ``kismet.device.base.datasize``,
                ``kismet.device.base.datasize.rrd``,
                ``kismet.device.base.first_time``,
                ``kismet.device.base.freq_khz_map``,
                ``kismet.device.base.frequency``,
                ``kismet.device.base.key``,
                ``kismet.device.base.last_time``,
                ``kismet.device.base.macaddr``,
                ``kismet.device.base.manuf``,
                ``kismet.device.base.mod_time``,
                ``kismet.device.base.name``,
                ``kismet.device.base.num_alerts``,
                ``kismet.device.base.packet.bin.250``,
                ``kismet.device.base.packet.bin.500``,
                ``kismet.device.base.packets.crypt``,
                ``kismet.device.base.packets.data``,
                ``kismet.device.base.packets.error``,
                ``kismet.device.base.packets.filtered``,
                ``kismet.device.base.packets.llc``,
                ``kismet.device.base.packets.rrd``,
                ``kismet.device.base.packets.rx``,
                ``kismet.device.base.packets.total``,
                ``kismet.device.base.packets.tx``,
                ``kismet.device.base.phyname``,
                ``kismet.device.base.seenby``,
                ``kismet.device.base.server_uuid``,
                ``kismet.device.base.signal``,
                ``kismet.device.base.tags``,
                ``kismet.device.base.type``.
        """
        valid_kwargs = ["last_time", "regex", "fields"]
        url = "devices/views/phydot11_accesspoints/devices.itjson"
        call_settings = {}
        if callback:
            call_settings["callback"] = callback
            if callback_args:
                call_settings["callback_args"] = callback_args
        call_settings["payload"] = {kword: kwargs[kword]
                                    for kword in valid_kwargs
                                    if kword in kwargs}
        for result in self.interact_yield("POST", url, **call_settings):
            yield result
