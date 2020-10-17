import unittest
from contrib.inteligent_store import IntelligentStoreList, StoreItem
import time
import random

class InteligentStoreTestCase(unittest.TestCase):

    def test_general_methods(self):
        s = IntelligentStoreList()

        v1 = StoreItem(1)
        s.append(v1)

        v2 = StoreItem(2)
        s.append(v2)

        self.assertEqual(v1, s.pop(0))
        self.assertEqual(v2, s.pop(0))

        self.assertEqual(s.len(), 0)
        with self.assertRaises(IndexError):
            s.pop(0)

        s.append(v1)
        s.append(v2)

        self.assertEqual(s.len(), 2)


    def test_sort(self):

        s = IntelligentStoreList()
        #for i in range(20):
        ##    s.append(StoreItem(random.randint(0, 1000)))
        #   time.sleep(random.randint(0, 100)/100)

        for item in [StoreItem(560, 1585425545.921279), StoreItem(73, 1585425546.0417), StoreItem(460, 1585425546.2822895), StoreItem(285, 1585425546.8830671), StoreItem(203, 1585425547.71406), StoreItem(545, 1585425548.1947637), StoreItem(254, 1585425548.4749916), StoreItem(676, 1585425548.805381), StoreItem(49, 1585425549.5162456), StoreItem(5, 1585425549.9667974), StoreItem(76, 1585425550.8179579), StoreItem(947, 1585425551.528875), StoreItem(710, 1585425552.4599833), StoreItem(577, 1585425552.860657), StoreItem(547, 1585425553.8620121), StoreItem(998, 1585425553.9224489), StoreItem(752, 1585425554.012917), StoreItem(553, 1585425554.6537871), StoreItem(643, 1585425554.984488), StoreItem(411, 1585425555.385272)]:
            s.append(item)


if __name__ == '__main__':
    unittest.main()
