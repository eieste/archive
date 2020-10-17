import time
from operator import attrgetter
from functools import cmp_to_key
import logging

log = logging.getLogger("InteligentStore")
log.setLevel(logging.DEBUG)

class StoreItem:

    def __init__(self, value, timestamp=None):
        assert type(value) == int
        if timestamp is None:
            timestamp = time.time()
        self._timestamp = timestamp
        self._value = value

    def __repr__(self):
        return 'StoreItem({}, {})'.format(self._value, self._timestamp)

    def __str__(self):
        return self._value

    def get_value(self):
        return self._value

    def get_timestamp(self):
        return self._timestamp


class SortMixin:

    @staticmethod
    def oldest_first(unsorted_data):

        def timestamp_cmp(a, b):
            return a.get_timestamp() < b.get_timestamp()

        data = list(unsorted_data)
        sorted_list = sorted(data, key=cmp_to_key(timestamp_cmp))
        return sorted_list


class IntelligentManager(SortMixin):

    def _cleanup(self):
        oldest_first = self.__class__.oldest_first(self._store)

                  # sec, min, 2min, 5min, 30min, 60min, 6h, 24h
        time_span  =[ 1, 60, 120, 300, 1800, 3600, 21600, 86400]
        span_summary = 0
        i = 1


        while len(oldest_first)-1 > i:
            item = oldest_first[i]
            next_item = oldest_first[i+1]

            span_summary += next_item.get_timestamp() - item.get_timestamp()
            i += 1
            print(span_summary/i)

        return


class IntelligentStoreList(IntelligentManager):

    def __init__(self, *args, **kwargs):
        self._store = []
        self._maxlen = 20
        pass

    def append(self, item):
        assert isinstance(item, StoreItem)

        # Run Cleanup whene 90% of STORE reached
        if len(self._store)/self._maxlen >= 0.9:
            log.debug("Run Cleanup")
            self._cleanup()

        self._store.append(item)

    def pop(self, index=0):
        return self._store.pop(index)

    def len(self):
        return len(self._store)
