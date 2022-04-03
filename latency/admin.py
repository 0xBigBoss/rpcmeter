from django.contrib import admin
from .models import Benchmark, Provider, Chain
# Register your models here.

admin.site.register(Benchmark)
admin.site.register(Provider)
admin.site.register(Chain)
