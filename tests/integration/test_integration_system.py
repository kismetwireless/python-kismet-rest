"""Test kismet_rest.System abstraction."""
import json

import pytest

import kismet_rest


class TestIntegrationSystem(object):
    """Test System()."""

    def create_authenticated_session(self):
        return kismet_rest.System(username="admin",
                                  password="passwordy",
                                  debug=True)

    def test_system_get_status(self):
        """Test getting system status."""
        system = self.create_authenticated_session()
        status = system.get_status()
        print(json.dumps(status, indent=4))
        assert isinstance(status, dict)

    def test_system_get_system_time(self):
        """Test retrieval of system time."""
        system = self.create_authenticated_session()
        system_time = system.get_system_time()
        print(json.dumps(system_time, indent=4))
        assert isinstance(system_time, dict)

    def test_system_get_system_time_isoformat(self):
        """Test getting time in ISO format."""
        system = self.create_authenticated_session()
        system_time = system.get_system_time("iso")
        print(system_time)
        assert isinstance(system_time, str)

    def test_system_get_system_time_badformat(self):
        """Test exception emitted from bad system time request."""
        system = self.create_authenticated_session()
        with pytest.raises(ValueError):
            system.get_system_time("bad")
