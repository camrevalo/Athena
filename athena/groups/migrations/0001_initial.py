# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=5000)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
                ('creator_username', models.CharField(max_length=5000)),
                ('topic', models.CharField(max_length=500)),
                ('group_type', models.CharField(default=b'Open', max_length=15, choices=[(b'Open', b'Open'), (b'Closed', b'Closed'), (b'Secret', b'Secret')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
