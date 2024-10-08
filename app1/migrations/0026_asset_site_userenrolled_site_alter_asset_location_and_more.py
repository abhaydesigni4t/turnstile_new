# Generated by Django 5.0.1 on 2024-07-19 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0025_remove_customuser_first_name_customuser_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='site',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app1.site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userenrolled',
            name='site',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app1.site'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=50),
        ),
        migrations.AlterField(
            model_name='asset',
            name='tag_id',
            field=models.IntegerField(),
        ),
    ]
