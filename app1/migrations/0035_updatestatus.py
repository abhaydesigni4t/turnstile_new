# Generated by Django 5.0.1 on 2024-08-19 11:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0034_alter_asset_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('dataset_updated', models.BooleanField(default=False)),
            ],
        ),
    ]