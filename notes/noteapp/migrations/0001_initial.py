# Generated by Django 4.1.1 on 2022-09-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Note",
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
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=150)),
                ("done", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("tags", models.ManyToManyField(to="noteapp.tag")),
            ],
        ),
    ]
