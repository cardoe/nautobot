# Generated by Django 3.2.18 on 2023-03-15 18:07

from django.db import migrations
import nautobot.dcim.models.locations


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0041_interface_ip_addresses_m2m"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="location",
            managers=[
                ("objects", nautobot.dcim.models.locations.LocationManager()),
            ],
        ),
    ]
