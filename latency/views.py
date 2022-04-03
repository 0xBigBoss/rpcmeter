from django.shortcuts import render
import json
from .models import Provider, Benchmark
from django.core import serializers

# Create your views here.
def index(request):

    data = {}
    for p in Provider.objects.all():
        benchmarks = Benchmark.objects.filter(provider=p)
        print(benchmarks)

        data[p.name] = json.loads(serializers.serialize("json", benchmarks))

    return render(request, "index.html", {
        "data": json.dumps(data),
        "providers": Provider.objects.all()
    })
