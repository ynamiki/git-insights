import datetime
import unittest

import utils

class TestDateRange(unittest.TestCase):

    def test(self):
        dates = utils.month_range_str(
            datetime.date(2017, 8, 14),
            datetime.date(2017, 12, 1))
        self.assertEqual(['2017-08', '2017-09', '2017-10', '2017-11'], dates)

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
