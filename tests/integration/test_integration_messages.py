"""Test kismet_rest.Messages abstraction."""

import kismet_rest


class TestIntegrationMessages(object):
    """Test Messages()."""

    def create_authenticated_session(self):
        """Return an authenticated session."""
        return kismet_rest.Messages(username="admin",
                                    password="passwordy",
                                    debug=True)

    def test_messages_yield_all(self):
        """Test getting messages."""
        messages = self.create_authenticated_session()
        all_messages = messages.all()
        for message in all_messages:
            assert isinstance(message, dict)
