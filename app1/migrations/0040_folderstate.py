# Generated by Django 5.0.1 on 2024-08-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_delete_datasetupdateflag'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('modification_time', models.DateTimeField()),
            ],
            options={
                'unique_together': {('folder_name', 'file_name')},
            },
        ),
    ]