# Generated by Django 5.1 on 2024-08-29 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("productname", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="media")),
                (
                    "productbrand",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "productcategory",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("description", models.TextField(max_length=255)),
                ("rating", models.DecimalField(decimal_places=2, max_digits=5)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("stock", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "_id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
