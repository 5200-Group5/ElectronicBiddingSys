# Generated by Django 4.2.6 on 2023-12-01 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("BiddingApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bid",
            fields=[
                (
                    "bid_id",
                    models.AutoField(
                        db_column="BidID", primary_key=True, serialize=False
                    ),
                ),
                ("price", models.IntegerField(db_column="Price")),
                ("status", models.CharField(db_column="Status", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "item_id",
                    models.AutoField(
                        db_column="ItemID", primary_key=True, serialize=False
                    ),
                ),
                ("description", models.TextField()),
                ("picture", models.CharField(blank=True, max_length=255, null=True)),
                ("category", models.CharField(max_length=255)),
                ("condition", models.CharField(db_column="Cond", max_length=255)),
                ("starting_price", models.IntegerField()),
                ("end_date", models.DateTimeField()),
                ("start_date", models.DateTimeField()),
            ],
            options={
                "db_table": "Item",
            },
        ),
        migrations.DeleteModel(
            name="CustomUser",
        ),
        migrations.AddField(
            model_name="bid",
            name="item",
            field=models.ForeignKey(
                db_column="ItemID",
                on_delete=django.db.models.deletion.CASCADE,
                to="BiddingApp.item",
            ),
        ),
        migrations.AddField(
            model_name="bid",
            name="user",
            field=models.ForeignKey(
                db_column="UserID",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]