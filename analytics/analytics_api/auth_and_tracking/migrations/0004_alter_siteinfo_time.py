# Generated by Django 4.2.7 on 2023-12-10 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_and_tracking", "0003_alter_siteinfo_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteinfo",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 12, 10, 20, 37, 0, 478659)
            ),
        ),
    ]
