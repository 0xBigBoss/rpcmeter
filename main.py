import datetime
import os
import signal
from threading import Thread
import time
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import requests
from django.conf import settings
from web3 import Web3

from models import *

# this is to prevent hard shutdowns where the process is interrupted halfway through etc.
quit_event = threading.Event()
signal.signal(signal.SIGINT, lambda *_args: quit_event.set())

# will change to some fancy environment or settings thing later.
DEFAULT_ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
NUM_REQUESTS = 10
HITS = 2
DELAY = 2
MEASURED_LATENCIES = [25, 50, 75, 90, 99]

def send_request(w3: Web3):
    start = time.time()
    w3.eth.get_balance(DEFAULT_ETH_ADDRESS)
    end = time.time()
    return end-start

# found this on stackoverflow, allows threading functions to give return values.
class Request(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def main_loop():
    while True:
        timestamp = datetime.datetime.now()
        num_requests = NUM_REQUESTS
        delay = DELAY
        hits = HITS
        measured_latencies = MEASURED_LATENCIES

        # iterates through providers
        for provider in Provider.select():
            w3 = Web3(Web3.HTTPProvider(provider.url))
            balance_times = np.array([])
            # how many times to smash the web3 provider ;).
            for i in range(hits):
                latencies = np.array([])
                threads = []
                for i in range(num_requests):
                    t = Request(target=send_request, args=[w3])
                    t.start()
                    threads.append(t)

                for t in threads:
                    latencies = np.append(latencies, t.join())
                balance_times = np.concatenate([balance_times, latencies])
                print(balance_times)
                time.sleep(delay)

            pxxDict: Dict[str, float] = dict()
            for pxx in measured_latencies:
                key = f"p{pxx}"
                pxxDict[key] = (
                    np.percentile(balance_times, pxx)
                )
            mean = (
                np.mean(balance_times)
            )
            benchmark = Benchmark.create(
                provider=provider,
                timestamp=timestamp,
                p25=pxxDict["p25"],
                p50=pxxDict["p50"],
                p75=pxxDict["p75"],
                p90=pxxDict["p90"],
                p99=pxxDict["p99"],
                mean=mean,
            )
            print(benchmark)
        if quit_event.is_set():
            print("safely shutting down")
            break
if __name__ == '__main__':
    main_loop()
