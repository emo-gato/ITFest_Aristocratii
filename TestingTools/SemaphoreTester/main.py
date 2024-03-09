from time import sleep

import requests as requests

for i in range(4):
    for j in range(3):
        requests.get(f"http://192.168.251.63/semaphore?s{i}={j}")
        print(f"s{i}-{j}\n")
        sleep(1)
for i in range(4):
    requests.get(f"http://192.168.251.63/semaphore?s{i}=0")