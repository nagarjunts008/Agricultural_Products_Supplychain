# Generated by Django 3.2 on 2021-04-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplychainapp', '0004_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='manufacturerid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]