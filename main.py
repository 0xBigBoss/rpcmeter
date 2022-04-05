import datetime
import os
import signal
import threading
import time
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import requests
from django.conf import settings
from web3 import Web3

from models import *

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
    for _ in range(num_requests):
        start = time.time()
        w3.eth.block_number
        end = time.time()
        height_times = np.append(height_times, end - start)
        time.sleep(wait_time)

    # Compute latencies to get balance
    for _ in range(num_requests):
        start = time.time()
        w3.eth.get_balance(DEFAULT_ETH_ADDRESS)
        end = time.time()
        balance_times = np.append(balance_times, end - start)
        time.sleep(wait_time)

    return LatencyData(height_times, balance_times)


def main_loop():
    while True:
        timestamp = datetime.datetime.now()
        num_requests = settings.NUM_REQUESTS
        wait_time = settings.WAIT_TIME
        measured_latencies = settings.MEASURED_LATENCIES
        for provider in Provider.select():
            latency_data = get_latency_data(provider.url, num_requests, wait_time)
            pxxDict: Dict[str, float] = dict()
            for pxx in measured_latencies:
                key = f"p{pxx}"
                pxxDict[key] = (
                    np.percentile(latency_data.height_time, pxx)
                    + np.percentile(latency_data.balance_times, pxx)
                ) / 2
            mean = (
                np.mean(latency_data.height_time) + np.mean(latency_data.balance_times)
            ) / 2
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
