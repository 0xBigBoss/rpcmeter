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

    region = models.ForeignKey('Region', models.DO_NOTHING)

    def __str__(self):
        return self.provider.name + " " + str(self.p50)

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
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    chain = models.ForeignKey(Chain, models.DO_NOTHING)
#    region = models.ForeignKey('Region', models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name + " " + self.chain.name

    class Meta:
        managed = True 
        db_table = 'provider'


class Region(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = True 
        db_table = 'region'
