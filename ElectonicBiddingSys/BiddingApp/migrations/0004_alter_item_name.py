# Generated by Django 4.2.7 on 2023-12-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BiddingApp', '0003_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
