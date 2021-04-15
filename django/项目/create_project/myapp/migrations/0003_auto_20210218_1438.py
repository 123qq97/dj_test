# Generated by Django 3.0.5 on 2021-02-18 06:38

from django.db import migrations, models
import django.db.models.manager
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200730_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str', tinymce.models.HTMLField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='student',
            managers=[
                ('stuobj', django.db.models.manager.Manager()),
            ],
        ),
    ]
