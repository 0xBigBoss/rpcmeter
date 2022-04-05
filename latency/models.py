from django.db import models


class Benchmark(models.Model):
    provider = models.ForeignKey("Provider", models.DO_NOTHING)
    timestamp = models.DateTimeField()

    p25 = models.FloatField()
    p50 = models.FloatField()
    p75 = models.FloatField()
    p90 = models.FloatField()
    p99 = models.FloatField()
    mean = models.FloatField()

    def __str__(self):
        return self.provider.name + " " + str(self.median)

    class Meta:
        managed = True
        db_table = "benchmark"


class Chain(models.Model):
    name = models.CharField(max_length=99999)
    chain_id = models.CharField(max_length=99999)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "chain"


class Provider(models.Model):
    name = models.CharField(max_length=99999)
    url = models.CharField(max_length=99999)
    symbol = models.CharField(max_length=99999)
    chain = models.ForeignKey(Chain, models.DO_NOTHING)

    def __str__(self):
        return self.name + " " + self.chain.name

    class Meta:
        managed = True
        db_table = "provider"
