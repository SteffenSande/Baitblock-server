# Generated by Django 2.1.4 on 2019-07-28 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articleScraper', '0002_auto_20190726_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('headline',)},
        ),
    ]
