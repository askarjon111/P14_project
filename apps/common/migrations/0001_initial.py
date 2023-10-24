# Generated by Django 4.2.3 on 2023-10-24 06:22

import apps.common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="File",
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
                ("created_at", models.DateTimeField(auto_created=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.common.utils.user_upload_path,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
