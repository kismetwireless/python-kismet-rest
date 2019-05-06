"""Integration tests for kismet_rest.BaseInterface."""
import json

import pytest

import kismet_rest


class TestIntegrationBaseInterface(object):
    """Test BaseInterface class."""

    def test_base_interface_instantiate_with_defaults(self):
        """Initiate BaseInterface with defaults, check attributes."""
        interface = kismet_rest.BaseInterface(username="admin",
                                              password="passwordy")
        assert interface
        assert interface.host_uri == "http://127.0.0.1:2501"
        assert interface.username == "admin"
        assert interface.password == "passwordy"

    def test_base_interface_get_kismet_version(self):
        """Test the ability to get version from Kismet."""
        interface = kismet_rest.BaseInterface(username="admin",
                                              password="passwordy")
        version = interface.get_kismet_version()
        print(json.dumps(version, indent=4))
        # We need to fix this when version is published in API.
        assert version
