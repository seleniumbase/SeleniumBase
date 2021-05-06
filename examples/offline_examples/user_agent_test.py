import pytest
from seleniumbase import BaseCase


@pytest.mark.offline  # Can be run with: "pytest -m offline"
class OfflineTests(BaseCase):
    def test_get_user_agent(self):
        self.open("data:,")
        user_agent = self.get_user_agent()
        print('\nUser Agent = "%s"' % user_agent)
