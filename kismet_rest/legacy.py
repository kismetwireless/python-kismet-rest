"""Kismet REST interface module.

(c) 2018 Mike Kershaw / Dragorn
Licensed under GPL2 or above.
"""

from .base_interface import BaseInterface

"""
The field simplification and pathing options are best described in the
developer docs for Kismet under docs/dev/webui_rest.md ; basically, they
allow for selecting specific fields from the tree and returning ONLY those
fields, instead of the entire object.

This will increase the speed of searches of large sets of data, and decrease
the time it takes for Kismet to return them.

Whenever possible this API will use the 'itjson' format for multiple returned
objects - this places a JSON object for each element in an array/vector
response as a complete JSON record followed by a newline; this allows for
parsing the JSON response without allocating the entire vector object in memory
first, and enables streamed-base parsing of very large responses.

Field Simplification Specification:

    Several endpoints in Kismet take a field filtering object.  These
    use a common specification:

    [
        field1,
        ...
        fieldN
    ]

    where a field may be a single-element string, consisting of a
    field name -or- a field path, such as:
        'kismet.device.base.channel'
        'kismet.device.base.signal/kismet.common.signal.last_signal_dbm'

    OR a field may be a two-value array, consisting of a field name or
    path, and a target name the field will be aliased to:

        ['kismet.device.base.channel', 'base.channel']
        ['kismet.device.base.signal/kismet.common.signal.last_signal_dbm',
            'last.signal']

    The fields in the returned device will be inserted as their final
    name - that is, from the first above example, the device will contain
        'kismet.device.base.channel' and 'kismet.common.signal.last_signal_dbm'
    and from the second example:
        'base.channel' and 'last.signal'

Filter Specification:

    Several endpoints in Kismet take a regex object.  These use a common
    specification:

    [
        [ multifield, regex ],
        ...
        [ multifield, regex ]
    ]

    Multifield is a field path specification which will automatically expand
    value-maps and vectors found in the path.  For example, the multifield
    path:
        'dot11.device/dot11.device.advertised_ssid_map/dot11.advertisedssid.ssid'

    would apply to all 'dot11.advertisedssid.ssid' fields in the ssid_map
    automatically.

    Regex is a basic string containing a regular expression, compatible with
    PCRE.

    To match on SSIDs:

    regex = [
    ['dot11.device/dot11.device.advertised_ssid_map/dot11.advertisedssid.ssid',
        '^SomePrefix.*' ]
    ]

    A device is included in the results if it matches any of the regular
    expressions.

"""


class KismetConnector(BaseInterface):
    """Kismet rest API."""

    def system_status(self):
        """Return system status.

        Note: This is superseded by :py:meth:`kismet_rest.System.get_status`
        """
        return self.interact("GET", "system/status.json")

    def device_summary(self, callback=None, cbargs=None):
        """Return a summary of all devices.

        Note: This is superseded by :py:meth:`kismet_rest.Devices.all`

        Deprecated API - now referenced as device_list(..)
        """
        return self.device_list(callback, cbargs)

    def device_list(self, callback=None, cbargs=None):
        """Return all fields of all devices.

        Note: This is superseded by :py:meth:`kismet_rest.Devices.all`

        This may be extremely memory and CPU intensive and should be avoided.
        Memory use can be reduced by providing a callback, which will be
        invoked for each device.

        In general THIS API SHOULD BE AVOIDED.  There are several potentially
        serious repercussions in querying all fields of all devices in a very
        high device count environment.

        It is strongly recommended that you use smart_device_list(...)
        """
        kwargs = {}
        url = "/devices/all_devices.itjson"
        if callback:
            kwargs = {"callback": callback,
                      "callback_args": cbargs}
        return self.interact("GET", url, True, **kwargs)

    def device_summary_since(self, ts=0, fields=None, callback=None,
                             cbargs=None):
        """
        device_summary_since(ts, [fields, callback, cbargs]) ->
            device summary list

        Note: This is superseded by :py:meth:`kismet_rest.Devices.all`

        Deprecated API - now referenced as smart_device_list(...)

        Return object containing summary of devices added or changed since ts
        and ts info
        """
        return self.smart_device_list(ts=ts, fields=fields, callback=callback,
                                      cbargs=cbargs)

    def smart_summary_since(self, ts=0, fields=None, regex=None, callback=None,
                            cbargs=None):
        """
        smart_summary_since([ts, fields, regex, callback, cbargs]) ->
            device summary list

        Note: This is superseded by :py:meth:`kismet_rest.Devices.all`

        Deprecated API - now referenced as smart_device_list(...)
        """
        return self.smart_device_list(ts=ts, fields=fields, regex=regex,
                                      callback=callback, cbargs=cbargs)

    def smart_device_list(self, ts=0, fields=None, regex=None, callback=None,
                          cbargs=None):
        """Return a list of devices.

        Note: This is superseded by :py:meth:`kismet_rest.Devices.all`

        Perform a 'smart' device list.  The device list can be manipulated in
        several ways:

            1.  Devices active since last timestamp.  By setting the 'ts'
                parameter, only devices which have been active since that
                timestamp will be returned.
            2.  Devices which match a regex, as defined by the regex spec above
            3.  Devices can be simplified to reduce the amount of work being
                done and number of fields being returned.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be returned as a
        vector.

        Args:
            ts (int): Unix epoch timestamp.
            fields (list): List of field names for matching.
            regex (str): Regular expression for field matching.
            callback (obj): Callback for processing search results.
            cbargs (list): List of arguments for callback.

        Returns:
            list: List of dictionary-type objects, which describe devices
                observed by Kismet.  Dictionary keys are:
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
                ``kismet.device.base.packet.bin.1000``,
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

        cmd = {}

        if fields:
            cmd["fields"] = fields

        if regex:
            cmd["regex"] = regex

        url = "devices/last-time/{}/devices.itjson".format(ts)
        kwargs = {"payload": cmd}
        if callback:
            kwargs = {"callback": callback,
                      "callback_args": cbargs,
                      "payload": cmd}
        print(url)
        return self.interact("POST", url, True, **kwargs)

    def device_list_by_mac(self, maclist, fields=None, callback=None,
                           cbargs=None):
        """List devices matching MAC addresses in maclist.

        Note: This method is deprecated.

        Use :py:meth:`kismet_rest.Devices.yield_by_mac` instead.

        MAC addresses may be
        complete MACs or masked MAC groups
        ("AA:BB:CC:00:00:00/FF:FF:FF:00:00:00").

        Returned devices can be summarized/simplified by the fields list.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be returned as a
        vector.
        """
        cmd = {}
        url = "devices/multimac/devices.itjson"
        if fields is not None:
            cmd["fields"] = fields

        cmd["devices"] = maclist

        if callback:
            return [result for result in
                    self.interact_yield("POST", url, payload=cmd,
                                        callback=callback,
                                        callback_args=cbargs, stream=True)]
        return [result for result in
                self.interact_yield("POST", url, payload=cmd, stream=True)]

    def dot11_clients_of(self, apkey, fields=None, callback=None, cbargs=None):
        """List clients of 802.11 AP.

        Note: This is superseded by
        :py:meth:`kismet_rest.Devices.dot11_clients_of`

        List devices which are clients of a given 802.11 access point, using
        the /phy/phy80211/clients-of endpoint.

        Returned devices can be summarized/simplified by the fields list.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be returned as a
        vector.
        """
        cmd = {}

        if fields is not None:
            cmd["fields"] = fields
        url = "phy/phy80211/clients-of/{}/clients.itjson".format(apkey)
        if callback:
            return [result for result in
                    self.interact_yield("POST", url, payload=cmd,
                                        callback=callback,
                                        callback_args=cbargs, stream=True)]
        return [result for result in
                self.interact_yield("POST", url, payload=cmd, stream=True)]

    def dot11_access_points(self, tstamp=None, regex=None, fields=None,
                            callback=None, cbargs=None):
        """Return a list of dot11 access points.

        Note: This is superseded by
        :py:meth:`kismet_rest.Devices.dot11_access_points`

        List devices which are considered to be 802.11 access points, using the
        /devices/views/phydot11_accesspoints/ view

        Returned devices can be summarized/simplified by the fields list.

        If a timestamp is given, only devices modified more recently than the
        timestamp (and matching any other conditions) will be returned.

        If a regex is given, only devices matching the regex (and any other
        conditions) will be returned.

        If a callback is given, it will be called for each device in the
        result. If no callback is provided, the results will be returned as a
        vector.

        Args:
            ts (int): Unix epoch timestamp
            regex (str): Regular expression for filtering results.
            fields (list): Fields for filtering.
            callback (obj): Callback for processing individual results.
            cbargs (list): List of arguments for callback.

        Return:
            list: List of dictionary-type objects which describe access points.
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
        cmd = {}

        if tstamp is not None:
            cmd["last_time"] = tstamp

        if regex is not None:
            cmd["regex"] = regex

        if fields is not None:
            cmd["fields"] = fields
        url = "devices/views/phydot11_accesspoints/devices.itjson"
        if callback:
            return [result for result in
                    self.interact_yield("POST", url, payload=cmd,
                                        callback=callback,
                                        callback_args=cbargs, stream=True)]
        return [result for result in
                self.interact_yield("POST", url, payload=cmd, stream=True)]

    def device(self, key, field=None, fields=None):
        """Wrap device_by_key.

        Deprecated.
        """
        return self.device_by_key(key, field, fields)

    def device_field(self, key, field):
        """Wrap device_by_key.

        Deprecated, prefer device_by_key with field.
        """
        return self.device_by_key(key, field=field)

    def device_by_key(self, key, field=None, fields=None):
        """Return a dictionary representing one device, identified by ``key``.

        Note: This is superseded by
        :py:meth:`kismet_rest.Devices.get_by_key`

        Fetch a complete device record by the Kismet key (unique key per Kismet
        session) or fetch a specific sub-field by path.

        If a field simplification set is passed in 'fields', perform a
        simplification on the result
        """
        if fields is None:
            if field is not None:
                field = "/" + field
            else:
                field = ""
            url = "devices/by-key/{}/device.json{}".format(key, field)
            result = self.interact("GET", url)
        else:
            payload = {"fields": fields}
            url = "devices/by-key/{}/device.json".format(key)
            result = self.interact("POST", url, payload=payload)
        return result

    def device_by_mac(self, mac, fields=None):
        """Return a list of all devices matching ``mac``.

        Deprecated.
        Use :py:meth:`kismet_rest.Devices.yield_by_mac` instead.

        Return a vector of all devices in all phy types matching the supplied
        MAC address; typically this will return a vector of a single device,
        but MAC addresses could overlap between phy types.

        If a field simplification set is passed in 'fields', perform a
        simplification on the result
        """
        if fields:
            cmd = {"fields": fields}
            url = "devices/by-mac/{}/devices.json".format(mac)
            return self.interact("POST", url, payload=cmd, stream=False)
        url = "devices/by-mac/{}/devices.json".format(mac)
        return self.interact("POST", url, stream=False)

    def datasources(self):
        """Return a list of data sources.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.all` instead.

        Return:
            list: List of dictionary-type objects, which describe data sources.
                Dictionary keys are:
                ``kismet.datasource.capture_interface``,
                ``kismet.datasource.channel``,
                ``kismet.datasource.channels``,
                ``kismet.datasource.definition``,
                ``kismet.datasource.dlt``,
                ``kismet.datasource.error``,
                ``kismet.datasource.error_reason``,
                ``kismet.datasource.hardware``,
                ``kismet.datasource.hop_channels``,
                ``kismet.datasource.hop_offset``,
                ``kismet.datasource.hopping``,
                ``kismet.datasource.hop_rate``,
                ``kismet.datasource.hop_shuffle``,
                ``kismet.datasource.hop_shuffle_skip``,
                ``kismet.datasource.hop_split``,
                ``kismet.datasource.info.amp_gain``,
                ``kismet.datasource.info.amp_type``,
                ``kismet.datasource.info.antenna_beamwidth``,
                ``kismet.datasource.info.antenna_gain``,
                ``kismet.datasource.info.antenna_orientation``,
                ``kismet.datasource.info.antenna_type``,
                ``kismet.datasource.interface``,
                ``kismet.datasource.ipc_binary``,
                ``kismet.datasource.ipc_pid``,
                ``kismet.datasource.linktype_override``,
                ``kismet.datasource.name``,
                ``kismet.datasource.num_error_packets``,
                ``kismet.datasource.num_packets``,
                ``kismet.datasource.packets_rrd``,
                ``kismet.datasource.passive``,
                ``kismet.datasource.paused``,
                ``kismet.datasource.remote``,
                ``kismet.datasource.retry``,
                ``kismet.datasource.retry_attempts``,
                ``kismet.datasource.running``,
                ``kismet.datasource.source_key``,
                ``kismet.datasource.source_number``,
                ``kismet.datasource.total_retry_attempts``,
                ``kismet.datasource.type_driver``,
                ``kismet.datasource.uuid``,
                ``kismet.datasource.warning``.

        """
        return self.interact("GET", "datasource/all_sources.json")

    def datasource_list_interfaces(self):
        """Return a list of all available interfaces.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.yield_interfaces` instead.
        """
        return self.interact("GET", "datasource/list_interfaces.json")

    def config_datasource_set_channel(self, uuid, channel):
        """Return ``True`` if operation was successful, ``False`` otherwise.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.set_channel` instead.

        Locks an data source to an 802.11 channel or frequency.  Channel
        may be complex channel such as "6HT40+".

        Requires valid login.

        """
        cmd = {"channel": channel}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def config_datasource_set_hop_rate(self, uuid, rate):
        """Set the hop rate of a specific data source by UUID.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.set_hop_rate` instead.

        Configures the hopping rate of a data source, while not changing the
        channels used for hopping.

        Requires valid login
        """
        cmd = {"rate": rate}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def config_datasource_set_hop_channels(self, uuid, rate, channels):
        """Set datasource hopping rate by UUID.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.set_hop_channels` instead.

        Configures a data source for hopping at 'rate' over a vector of
        channels.

        Requires valid login
        """
        cmd = {"rate": rate,
               "channels": channels}
        url = "datasource/by-uuid/{}/set_channel.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def config_datasource_set_hop(self, uuid):
        """Configure a source for hopping.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.set_hop` instead.

        Uses existing source hop / channel list / etc attributes.

        Requires valid login
        """
        cmd = {"hop": True}
        url = "datasource/by-uuid/{}/set_hop.cmd".format(uuid)
        return self.interact("POST", url, payload=cmd, only_status=True)

    def add_datasource(self, source):
        """Add a new source to Kismet.

        Deprecated.
        Use :py:meth:`kismet_rest.Datasources.add` instead.

        source is a standard source definition.

        Requires valid login.

        Return:
            bool: Success
        """
        cmd = {"definition": source}

        return self.interact("POST", "datasource/add_source.cmd",
                             only_status=True, payload=cmd)

    def define_alert(self, name, description, rate="10/min", burst="1/sec",
                     phyname=None):
        """
        define_alert(name, description, rate, burst) -> Boolean

        Deprecated.
        Use :py:meth:`kismet_rest.Alerts.define` instead.

        LOGIN REQUIRED

        Define a new alert.  This alert can then be triggered on external
        conditions via raise_alert(...)

        Phyname is optional, and links the alert to a specific PHY type.

        Rate and Burst are optional rate and burst limits.
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

        Deprecated.
        Use :py:meth:`kismet_rest.Alerts.raise` instead.

        LOGIN REQUIRED

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

    def alerts(self, ts_sec=0, ts_usec=0):
        """Return alert object.

        Deprecated.
        Use :py:meth:`kismet_rest.Alerts.all` instead.

        Fetch alert object, containing metadata and list of alerts, optionally
        filtered to alerts since a given timestamp

        Args:
            ts_sec (int): Timestamp seconds (Unix epoch)
            ts_usec (int): Timestamp microseconds

        Return:
            dict: Dictionary containing metadata and a list of alerts. Keys
                represented in output: ``'kismet.alert.timestamp``,
                ``kismet.alert.list``.
        """
        url = "alerts/last-time/{}.{}/alerts.json".format(ts_sec, ts_usec)
        return self.interact("GET", url)

    def messages(self, ts_sec=0, ts_usec=0):
        """Return message object.

        Deprecated.
        Use :py:meth:`kismet_rest.Messages.all` instead.

        Fetch message object, containing metadata and list of messages,
        optionally filtered to messages since a given timestamp

        Args:
            ts_sec (int): Timestamp seconds (Unix epoch)
            ts_usec (int): Timestamp microseconds

        Return:
            dict: Dictionary containing metadata and a list of messages.
                Top-level keys: ``kismet.messagebus.timestamp``,
                ``kismet.messagebus.list``
        """
        url = "messagebus/last-time/{}.{}/messages.json".format(ts_sec,
                                                                ts_usec)
        return self.interact("GET", url)

    def location(self):
        """Return the gps location.

        Deprecated.
        Use :py:meth:`kismet_rest.GPS.current_location` instead.

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


if __name__ == "__main__":
    print(KismetConnector().system_status())
