# Generated by Django 3.2.4 on 2021-12-02 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='watchlist',
            new_name='item',
        ),
    ]
