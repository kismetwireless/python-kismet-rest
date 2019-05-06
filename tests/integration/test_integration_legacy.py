"""Integration tests for legacy KismetConnector object."""
import pprint
import sys

import pytest

import kismet_rest
from kismet_rest.exceptions import KismetLoginException


class TestIntegrationLegacy(object):
    def instantiate_kismet_connector_noauth(self):
        return kismet_rest.KismetConnector(debug=True)

    def instantiate_kismet_connector_auth(self):
        return kismet_rest.KismetConnector(username="admin",
                                           password="passwordy",
                                           debug=True)

    def printy_callback(self, json_object):
        print("Printing via a callback...")
        pprint.pprint(json_object)

    def printy_callback_args(self, json_object, arg1, arg2):
        print("Printing via a callback...")
        print("{} {}".format(arg1, arg2))
        pprint.pprint(json_object)

    def test_kismet_connector_instantiate(self):
        assert self.instantiate_kismet_connector_noauth()

    def test_kismet_connector_list_devices(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.device_summary()
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    def test_kismet_connector_list_devices_with_callback(self):
        connector = self.instantiate_kismet_connector_noauth()
        callback = self.printy_callback
        result = connector.device_summary(callback)
        assert result == []

    def test_kismet_connector_list_devices_with_callback_args(self):
        connector = self.instantiate_kismet_connector_noauth()
        callback = self.printy_callback_args
        cbargs = ["First_arg", "somesuch other second thing..."]
        result = connector.device_summary(callback, cbargs)
        assert result == []

    def test_kismet_connector_device_summary_since(self):
        connector = self.instantiate_kismet_connector_noauth()
        callback = self.printy_callback
        result = connector.device_summary_since()
        assert isinstance(result, list)

    def test_kismet_connector_smart_device_summary_since(self):
        connector = self.instantiate_kismet_connector_noauth()
        callback = self.printy_callback
        result = connector.smart_summary_since()
        assert isinstance(result, list)

    def test_kismet_connector_get_gps(self):
        connector = self.instantiate_kismet_connector_auth()
        result = connector.location()
        print(result.keys())
        assert isinstance(result, dict)

    def test_kismet_connector_messages(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.messages()
        print(result)
        assert isinstance(result, dict)

    def test_kismet_connector_alerts(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.alerts()
        print(result.keys())
        assert isinstance(result, dict)

    def test_kismet_connector_datasource_list_interfaces(self):
        connector = self.instantiate_kismet_connector_auth()
        interfaces = [x for x in connector.datasource_list_interfaces()]
        assert isinstance(interfaces, list)

    def test_kismet_connector_datasources(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.datasources()
        assert isinstance(result, list)

    def test_kismet_connector_dot11_access_points(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.dot11_access_points()
        print(sorted(result[0].keys()))
        assert isinstance(result, list)

    def test_kismet_connector_smart_device_list(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.smart_device_list()
        print(sorted(result[0].keys()))
        assert isinstance(result, list)

    def test_kismet_connector_system_status(self):
        connector = self.instantiate_kismet_connector_noauth()
        result = connector.system_status()
        print(result)
        assert isinstance(result, dict)

    def test_kismet_connector_list_devices_by_key(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_device = connector.smart_device_list()[0]
        target_device_key = target_device["kismet.device.base.key"]
        result = connector.device(target_device_key)
        print(result)
        assert isinstance(result, dict)

    def test_kismet_connector_list_device_by_mac(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_device = connector.smart_device_list()[0]
        target_device_key = target_device["kismet.device.base.macaddr"]
        result = connector.device_by_mac(target_device_key)
        print(result)
        assert isinstance(result, list)

    def test_kismet_connector_dot11_clients_of(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_ap = connector.dot11_access_points()[0]["kismet.device.base.key"]  # NOQA
        devices = connector.dot11_clients_of(target_ap)
        print(target_ap)
        print(devices)
        assert isinstance(devices, list)

    def test_kismet_connector_list_devices_by_key_field(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_device = connector.smart_device_list()[0]
        target_device_key = target_device["kismet.device.base.key"]
        field = "kismet.device.base.type"
        result = connector.device(target_device_key, field)
        print(result)
        print(type(result))
        if sys.version_info[0] < 3:
            assert isinstance(result, basestring)
        else:
            assert isinstance(result, str)

    def test_kismet_connector_raise_alert(self):
        connector = self.instantiate_kismet_connector_auth()
        name = "ScaryAlert"
        text = "Super scary things on your wireless."
        assert connector.raise_alert(name, text)

    def test_kismet_connector_define_alert(self):
        connector = self.instantiate_kismet_connector_noauth()
        name = "ScaryAlert"
        description = "Super scary things on your wireless."
        assert connector.define_alert(name, description)

    def test_kismet_connector_add_datasource_fail(self):
        connector = self.instantiate_kismet_connector_noauth()
        source = "MY_DATA_SOURCE"
        with pytest.raises(KismetLoginException):
            connector.add_datasource(source)

    def test_kismet_connector_config_datasource_set_hop_fail(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_datasource = connector.datasources()[0]
        uuid = target_datasource["kismet.datasource.uuid"]
        with pytest.raises(KismetLoginException):
            connector.config_datasource_set_hop(uuid)

    def test_kismet_connector_config_datasource_set_hop_channels(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_datasource = connector.datasources()[0]
        uuid = target_datasource["kismet.datasource.uuid"]
        rate = "123"
        channels = [1, 2, 3]
        with pytest.raises(KismetLoginException):
            connector.config_datasource_set_hop_channels(uuid, rate, channels)

    def test_kismet_connector_config_datasource_set_hop_rate(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_datasource = connector.datasources()[0]
        uuid = target_datasource["kismet.datasource.uuid"]
        rate = "123"
        with pytest.raises(KismetLoginException):
            connector.config_datasource_set_hop_rate(uuid, rate)

    def test_kismet_connector_config_datasource_set_channel(self):
        connector = self.instantiate_kismet_connector_noauth()
        target_datasource = connector.datasources()[0]
        uuid = target_datasource["kismet.datasource.uuid"]
        channel = "1"
        with pytest.raises(KismetLoginException):
            connector.config_datasource_set_channel(uuid, channel)

    def test_kismet_connector_add_datasource(self):
        connector = self.instantiate_kismet_connector_auth()
        source = "/export/kismet.pcap:name=reconsume_this_yo"
        connector.login()
        connector.add_datasource(source)
