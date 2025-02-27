# Generated by Django 3.1.13 on 2021-08-16 15:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0011_fileattachment_fileproxy"),
    ]

    operations = [
        migrations.CreateModel(
            name="HealthCheckTestModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=128)),
            ],
        ),
    ]
