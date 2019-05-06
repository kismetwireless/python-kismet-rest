"""Test the Utility class."""
import kismet_rest


class TestUnitUtility(object):
    """Test the Utility class."""

    def test_unit_utility_build_full_url_simple(self):
        """Test the URL builder with relative path."""
        base = "http://localhost:2501"
        path = "v1/devices"
        control = "http://localhost:2501/v1/devices"
        result = kismet_rest.Utility.build_full_url(base, path)
        assert result == control

    def test_unit_utility_build_full_url_leading_slash(self):
        """Test the URL builder's handling of a leading slash."""
        base = "http://localhost:2501"
        path = "/v1/devices"
        control = "http://localhost:2501/v1/devices"
        result = kismet_rest.Utility.build_full_url(base, path)
        assert result == control

    def test_unit_utility_build_full_url_double_leading_slash(self):
        """Test building URL with double leading slash."""
        base = "http://localhost:2501"
        path = "//v1/devices"
        control = "http://localhost:2501/v1/devices"
        result = kismet_rest.Utility.build_full_url(base, path)
        assert result == control

    def test_unit_utility_build_full_url_proxypath(self):
        """Test URL building with proxy path."""
        base = "http://frontend.proxy:2501/kismetpath/"
        path = "v1/devices"
        control = "http://frontend.proxy:2501/kismetpath/v1/devices"
        result = kismet_rest.Utility.build_full_url(base, path)
        assert result == control

    def test_unit_utility_build_full_url_proxypath_no_trailing_slash(self):
        """Test building URL with proxy path and no trailing slash."""
        base = "http://frontend.proxy:2501/kismetpath"
        path = "v1/devices"
        control = "http://frontend.proxy:2501/kismetpath/v1/devices"
        result = kismet_rest.Utility.build_full_url(base, path)
        assert result == control
