# Generated by Django 5.0.1 on 2024-05-16 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_userenrolled_facial_data_delete_facialimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='preshift/')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
