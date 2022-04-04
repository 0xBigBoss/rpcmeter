# Generated by Django 4.0 on 2022-04-02 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Benchmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("p90", models.FloatField()),
                ("p70", models.FloatField()),
                ("p30", models.FloatField()),
                ("median", models.FloatField()),
                ("mean", models.FloatField()),
            ],
            options={
                "db_table": "benchmark",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=99999)),
                ("chain_id", models.CharField(max_length=99999)),
            ],
            options={
                "db_table": "chain",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Provider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=99999)),
                ("url", models.CharField(max_length=99999)),
                ("symbol", models.CharField(max_length=99999)),
            ],
            options={
                "db_table": "provider",
                "managed": False,
            },
        ),
    ]
