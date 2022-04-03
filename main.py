from models import *
from web3 import Web3
import time
import numpy as np
import requests
import datetime
import signal
import threading

quit_event = threading.Event()
signal.signal(signal.SIGINT, lambda *_args: quit_event.set())

def latency(url):
    w3 = Web3(Web3.HTTPProvider(url))
    height_times = np.array([])
    account_times = np.array([])

    for i in range(100):
        start = time.time()
        w3.eth.block_number
        end = time.time()
        height_times = np.append(height_times, end-start)
        time.sleep(0.05)

    for i in range(100):
        start = time.time()
        w3.eth.get_balance("0x0000000000000000000000000000000000000000")
        end = time.time()
        account_times = np.append(account_times, end-start)
        time.sleep(0.05)

    return height_times, account_times

while True:
    timestamp = datetime.datetime.now()

    for provider in Provider.select():
        height_times, account_times = latency(provider.url)

        print(height_times, account_times)

        p90 = (np.percentile(height_times, 90)+np.percentile(account_times, 90))/2
        p70 = (np.percentile(height_times, 70)+np.percentile(account_times, 70))/2
        p30 = (np.percentile(height_times, 30)+np.percentile(account_times, 30))/2
        median = (np.percentile(height_times, 50)+np.percentile(account_times, 50))/2
        mean = (np.mean(height_times)+np.mean(account_times))/2
        print(provider.name, p90, p70, p30, median, mean)

        benchmark = Benchmark.create(provider=provider, timestamp=timestamp, p90=p90, p70=p70, p30=p30, median=median, mean=mean)
    if quit_event.is_set():
        print("safely shutting down")
        break

    #time.sleep(180)
