# Generated by Django 3.2.5 on 2021-07-26 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0002_auto_20210726_1333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ['part']},
        ),
    ]
