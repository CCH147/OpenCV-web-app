# Generated by Django 4.1 on 2024-03-11 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysite", "0005_enddate_delete_ghtrashdata_alter_alldata_year"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("Original", models.ImageField(blank=True, null=True, upload_to="")),
                ("Img", models.ImageField(blank=True, null=True, upload_to="")),
            ],
        ),
    ]
