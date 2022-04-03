from peewee import *

db = SqliteDatabase('db')

class Chain(Model):
    name = CharField()
    chain_id = CharField()

    class Meta:
        database = db

class Provider(Model):
    name = CharField()
    url = CharField()
    symbol = CharField()
    chain = ForeignKeyField(Chain, backref='chain')

    class Meta:
        database = db

class Benchmark(Model):
    provider = ForeignKeyField(Provider, backref='provider')
    timestamp = DateTimeField()
    p90 = FloatField()
    p70 = FloatField()
    p30 = FloatField()
    median = FloatField()
    mean = FloatField()

    class Meta:
        database = db 

db.connect()
db.create_tables([Chain, Provider, Benchmark])
