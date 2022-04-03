from django.db import models

class Benchmark(models.Model):
    provider = models.ForeignKey('Provider', models.DO_NOTHING)
    timestamp = models.DateTimeField()
    p90 = models.FloatField()
    p70 = models.FloatField()
    p30 = models.FloatField()
    median = models.FloatField()
    mean = models.FloatField()

    class Meta:
        managed = False
        db_table = 'benchmark'


class Chain(models.Model):
    name = models.CharField(max_length=99999)
    chain_id = models.CharField(max_length=99999)

    class Meta:
        managed = False
        db_table = 'chain'


class Provider(models.Model):
    name = models.CharField(max_length=99999)
    url = models.CharField(max_length=99999)
    symbol = models.CharField(max_length=99999)
    chain = models.ForeignKey(Chain, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'provider'
