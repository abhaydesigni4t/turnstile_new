# Generated by Django 5.0.1 on 2024-08-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_timeschedule_site_turnstile_s_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userenrolled',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')], default='pending', max_length=100),
        ),
    ]
