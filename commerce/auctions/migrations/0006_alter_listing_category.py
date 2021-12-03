# Generated by Django 3.2.4 on 2021-08-13 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210813_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), ('entertainment', 'Entertainment'), ('automotive', 'Automotive'), ('furniture', 'Furniture'), ('others', 'Others'), ('na', '-')], default='na', max_length=64),
        ),
    ]