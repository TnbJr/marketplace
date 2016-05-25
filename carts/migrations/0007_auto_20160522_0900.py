# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_cart_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(decimal_places=2, default=9.0, max_digits=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=9.0, max_digits=50),
            preserve_default=False,
        ),
    ]
