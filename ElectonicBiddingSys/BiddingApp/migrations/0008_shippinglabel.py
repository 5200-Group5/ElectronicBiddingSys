# Generated by Django 4.2.6 on 2023-12-06 06:36

import BiddingApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("BiddingApp", "0007_alter_item_creator"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingLabel",
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
                (
                    "tracking_number",
                    models.CharField(
                        default=BiddingApp.models.generate_tracking_number,
                        max_length=10,
                        unique=True,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_labels",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipping_labels",
                        to="BiddingApp.item",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="won_items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]