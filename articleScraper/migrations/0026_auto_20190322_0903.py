# Generated by Django 2.1.4 on 2019-03-22 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articleScraper', '0025_article_article'),
    ]

    operations = [
        migrations.RenameField(
            model_name='child',
            old_name='parent',
            new_name='content',
        ),
    ]