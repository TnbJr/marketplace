# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-05 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_sales_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='hah', unique=True),
            preserve_default=False,
        ),
    ]
