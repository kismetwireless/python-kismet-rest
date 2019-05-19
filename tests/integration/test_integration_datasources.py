"""Test kismet_rest.Datasources abstraction."""
import kismet_rest


class TestIntegrationDatasources(object):
    """Test Datasources()."""

    def create_authenticated_session(self):
        """Return an authenticated session."""
        return kismet_rest.Datasources(username="admin",
                                       password="passwordy",
                                       debug=True)

    def test_datasources_all(self):
        """Test getting datasources."""
        datasources = self.create_authenticated_session()
        all_sources = datasources.all()
        for source in all_sources:
            assert isinstance(source, dict)

    def test_datasources_interfaces(self):
        """Test getting datasources."""
        datasources = self.create_authenticated_session()
        all_sources = datasources.interfaces()
        for source in all_sources:
            assert isinstance(source, dict)

    def test_datasource_add_datasource(self):
        """Add pcap file datasource."""
        datasources = self.create_authenticated_session()
        source = "/export/kismet.pcap:name=reconsume_this_yo"
        datasources.login()
        datasources.add(source)
