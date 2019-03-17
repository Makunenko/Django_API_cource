# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-03-02 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import samples.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_id', models.TextField()),
                ('system_composition', models.TextField()),
                ('sample_treatment', models.TextField(blank=True, null=True)),
                ('sample_xrd', models.FileField(blank=True, null=True, upload_to=samples.models.upload_sample_xrd)),
            ],
        ),
    ]