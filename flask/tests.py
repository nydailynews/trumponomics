import os
import application
import unittest
import tempfile
from datetime import datetime

class SiteTestCase(unittest.TestCase):

    def setUp(self):
        application.app.config['TESTING'] = True
        self.app = application.app.test_client()

    def tearDown(self):
        pass

    def valid_response(self, url):
        response = self.app.get(url)
        if response.status_code >= 400:
            print url, response.status_code
        assert response.status_code < 400

    def test_responses(self):
        today = datetime.today()
        for url in self.app.application.url_map.iter_rules():
            # Process the variables with static values in the urls:
            url = url.__str__()
            url = url.replace('<detail>', 'gdp-growth')
            if '<shortcut>' in url or 'static' in url:
                continue
            print url
            self.valid_response(url)

if __name__ == '__main__':
    unittest.main()
