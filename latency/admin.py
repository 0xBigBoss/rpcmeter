from django.contrib import admin

from .models import Benchmark, Chain, Provider, Region

# Register your models here.

admin.site.register(Benchmark)
admin.site.register(Provider)
admin.site.register(Chain)
admin.site.register(Region)

