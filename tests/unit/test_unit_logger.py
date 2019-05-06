"""Test Logger."""
import kismet_rest


class TestUnitLogger(object):
    """Test the Logger."""

    def test_all_log_methods(self):
        """Test each log level."""
        logger = kismet_rest.Logger()
        logger.set_info()
        logger.set_debug()
        for x in [logger.critical, logger.error, logger.warn, logger.info,
                  logger.debug]:
            x("test message")
        assert True
