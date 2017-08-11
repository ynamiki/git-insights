import datetime
import unittest

import utils

class TestGetDomain(unittest.TestCase):

    def test(self):
        data = [
            ('foo@example.org', 'example.org'),
            ('foo@bar.example.org', 'bar.example.org'),
            ('foo@example.com', 'example.com'),
            ('foo@bar.example.com', 'example.com'),
            ('foo@users.noreply.github.com', 'users.noreply.github.com')
        ]
        for d in data:
            self.assertEqual(d[1], utils.get_domain(d[0]))

if __name__ == '__main__':
    unittest.main()
