# Generated by Django 3.2 on 2021-05-01 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplychainapp', '0015_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='logistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]