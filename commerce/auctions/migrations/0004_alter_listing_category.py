# Generated by Django 3.2.4 on 2021-08-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), ('entertainment', 'Entertainment'), ('automotive', 'Automotive'), ('others', 'Others'), ('na', '-')], default='na', max_length=64),
        ),
    ]
