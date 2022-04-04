from django.shortcuts import render
import json
from .models import Provider, Benchmark, Chain
from django.core import serializers

# Create your views here.
def chain(request, chain):
    data = {}

    chain = Chain.objects.get(name=chain.lower())

    for p in Provider.objects.filter(chain=chain):
        benchmarks = Benchmark.objects.filter(provider=p)
        print(benchmarks)

        data[p.name] = json.loads(serializers.serialize("json", benchmarks))

    return render(request, "chain.html", {
        "data": json.dumps(data),
        "providers": Provider.objects.all(),
        "chain": chain.name.capitalize()
    })


def index(request):
    return render(request, "index.html", {
        "chains": Chain.objects.all()
    })
