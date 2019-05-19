"""Test kismet_rest.Alerts abstraction."""
import pprint

import kismet_rest


class TestIntegrationAlerts(object):
    """Test Alerts()."""

    def test_alerts_all(self):
        """Test getting alerts."""
        alerts = kismet_rest.Alerts(username="admin", password="passwordy")
        all_alerts = alerts.all()
        for alert in all_alerts:
            assert isinstance(alert, dict)

    def test_alerts_callback(self):
        """Test alerts with callback."""
        alerts = kismet_rest.Alerts(username="admin", password="passwordy")
        callback = pprint.pprint
        all_alerts = alerts.all(callback)
        assert all_alerts
        for alert in all_alerts:
            assert isinstance(alert, None)
