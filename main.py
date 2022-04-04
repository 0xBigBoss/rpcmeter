import datetime
import signal
import threading
import time

import numpy as np
import requests
from web3 import Web3
from typing import List, Dict

from models import *

quit_event = threading.Event()
signal.signal(signal.SIGINT, lambda *_args: quit_event.set())

DEFAULT_ETH_ADDRESS = "0x0000000000000000000000000000000000000000"

@dataclass
class LatencyData:
    height_time: List[float]
    balance_times: List[float]

def get_latency_data(url: str, num_requests: int, wait_time: int) -> LatencyData:
    w3 = Web3(Web3.HTTPProvider(url))
    height_times = np.array([])
    balance_times = np.array([])

    # Compute latencies to get latest block height
    for i in range(num_requests):
        start = time.time()
        w3.eth.block_number
        end = time.time()
        height_times = np.append(height_times, end - start)
        time.sleep(wait_time)

    # Compute latencies to get balance
    for i in range(num_requests):
        start = time.time()
        w3.eth.get_balance(DEFAULT_ETH_ADDRESS)
        end = time.time()
        balance_times = np.append(balance_times, end - start)
        time.sleep(wait_time)

    return LatencyData(height_time, balance_times)

while True:
    timestamp = datetime.datetime.now()
    num_rquests = os.getenv("NUM_REQUESTS")
    wait_time = os.getenv("WAIT_TIME")
    measured_latencies = os.getenv("MEASURED_LATENCIES")

    for provider in Provider.select():
        latency_data = get_latency_data(provider.url, num_rquests, wait_time)
        pxx: Dict[s] = Dict[]
        for pxx in measured_latencies:
            key = f'p{pxx}'
            # BAD
            pxx[key] = average(np.percentile(height_times, pxx), np.percentile(balance_times, pxx))
        mean = (np.mean(height_times) + np.mean(balance_times)) / 2
        benchmark = Benchmark.create(
            provider=provider,
            timestamp=timestamp,
            p25=pxx['p25'],
            p50=pxx['p75'],
            p75=pxx['p75'],
            p90=pxx['p90'],
            p99=pxx['p99'],
            mean=mean,
        )
        print(benchmark)
    if quit_event.is_set():
        print("safely shutting down")
        break
