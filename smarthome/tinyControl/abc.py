import logging
from contrib.inteligent_store import StoreItem, IntelligentStoreList
from contrib.inteligent_store import StoreItem, IntelligentStoreList
import random
import time

logging.basicConfig(level=logging.DEBUG)

s = IntelligentStoreList()
for i in range(20):
    s.append(StoreItem(random.randint(0, 1000)))
    time.sleep(random.randint(90, 100)/100)


for item in [StoreItem(109, 1585426400.0421062), StoreItem(314, 1585426401.033158), StoreItem(924, 1585426402.0244496), StoreItem(184, 1585426402.9857013), StoreItem(722, 1585426403.9569418), StoreItem(910, 1585426404.8781805), StoreItem(781, 1585426405.7793407), StoreItem(838, 1585426406.7406158), StoreItem(796, 1585426407.6418366), StoreItem(789, 1585426408.6029017), StoreItem(353, 1585426409.6039844), StoreItem(785, 1585426410.5752454), StoreItem(562, 1585426411.5165033), StoreItem(315, 1585426412.4475927), StoreItem(584, 1585426413.348812), StoreItem(792, 1585426414.2799075), StoreItem(66, 1585426415.251053), StoreItem(545, 1585426416.2023244), StoreItem(937, 1585426417.1836164), StoreItem(432, 1585426418.1055388)]:
    s.append(item)
