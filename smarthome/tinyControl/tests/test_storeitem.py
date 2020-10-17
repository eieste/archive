import unittest
from contrib.inteligent_store import StoreItem


class StoreItemTestCase(unittest.TestCase):

    def test_init(self):
        s = StoreItem(123, 1)
        self.assertEqual(s.get_value(), 123)
        self.assertEqual(s.get_timestamp(), 1)

        with self.assertRaises(AssertionError):
            s = StoreItem("asdf", 1)


if __name__ == '__main__':
    unittest.main()
