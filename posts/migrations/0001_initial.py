# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-22 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('content', models.TextField()),
                ('source', models.URLField(blank=True, null=True)),
                ('draft', models.BooleanField(default=False)),
                ('published', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('categories', models.CharField(choices=[('news', 'News'), ('entertainmet', 'Entertainmet'), ('other', 'Other')], default='Entertainmet', max_length=50)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
