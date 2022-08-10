import json

from django.contrib import admin
from django.core import serializers
from django.shortcuts import render

from .models import Benchmark, Chain, Provider, Region


# Create your views here.
def chain(request, chain, region):
    data = {}

    chain = Chain.objects.get(name=chain.lower())
    region = Region.objects.get(name=region.lower())

    for p in Provider.objects.filter(region=region, chain=chain):
        benchmarks = Benchmark.objects.filter(provider=p)
        data[p.name] = json.loads(serializers.serialize("json", benchmarks))

    return render(
        request,
        "chain.html",
        {
            "data": json.dumps(data),
            "providers": Provider.objects.all(),
            "chain": chain.name.capitalize(),
        },
    )

# Create your views here.
def regions(request, chain):
    data = {}

    regions = Region.objects.all()
    print(regions)

    return render(
        request,
        "region.html",
        {
            "regions": regions,
            "chain": chain.capitalize(),
        },
    )

def index(request):
    return render(request, "index.html", {"chains": Chain.objects.all()})
