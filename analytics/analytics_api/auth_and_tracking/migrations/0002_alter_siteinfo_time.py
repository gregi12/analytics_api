# Generated by Django 4.2.7 on 2023-12-10 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_and_tracking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteinfo",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 12, 10, 15, 20, 49, 707622)
            ),
        ),
    ]
