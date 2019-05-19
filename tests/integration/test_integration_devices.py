"""Test kismet_rest.Devices abstraction."""
import pprint

import kismet_rest


class TestIntegrationDevices(object):
    """Test Devices()."""

    def create_authenticated_session(self):
        return kismet_rest.Devices(username="admin",
                                   password="passwordy",
                                   debug=True)

    def test_devices_all(self):
        """Test getting devices."""
        devices = self.create_authenticated_session()
        all_devices = devices.all()
        for device in all_devices:
            assert isinstance(device, dict)

    def test_devices_callback(self):
        """Test devices with callback."""
        devices = self.create_authenticated_session()
        callback = pprint.pprint
        all_devices = devices.all(callback)
        assert all_devices
        for device in all_devices:
            assert isinstance(device, None)

    def test_devices_by_mac(self):
        """Test getting devices."""
        devices = self.create_authenticated_session()
        device_list = ["00:00:00:00:00:00/00:00:00:00:00:00"]
        all_devices = devices.by_mac(devices=device_list)
        for device in all_devices:
            assert isinstance(device, dict)

    def test_devices_by_mac_callback(self):
        """Test devices with callback."""
        devices = self.create_authenticated_session()
        callback = pprint.pprint
        device_list = ["00:00:00:00:00:00/00:00:00:00:00:00"]
        all_devices = devices.by_mac(callback, devices=device_list)
        assert all_devices
        for device in all_devices:
            assert isinstance(device, None)

    def test_devices_dot11_clients_of(self):
        """Test getting clients of device."""
        devices = self.create_authenticated_session()
        target_devices = [x for x in devices.all()]
        target = target_devices[0]["kismet.device.base.key"]
        for client in devices.dot11_clients_of(target):
            assert isinstance(client, dict)

    def test_devices_dot11_access_points(self):
        """Test getting dot11 access points."""
        devices = self.create_authenticated_session()
        for access_point in devices.dot11_access_points():
            assert isinstance(access_point, dict)

    def test_get_device_by_key(self):
        """Test getting clients of device."""
        devices = self.create_authenticated_session()
        target_devices = [x for x in devices.all()]
        target = target_devices[0]["kismet.device.base.key"]
        result = devices.by_key(target)
        assert isinstance(result, dict)
