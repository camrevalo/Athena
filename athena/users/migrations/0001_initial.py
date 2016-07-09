# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.CharField(default=b'Paste image URL here', max_length=5000)),
                ('school', models.CharField(default=b'school', max_length=500)),
                ('isTeacher', models.BooleanField(default=False)),
                ('firstName', models.CharField(default=b'first name', max_length=500)),
                ('lastName', models.CharField(default=b'last name', max_length=500)),
                ('downvotedAnswers', models.ManyToManyField(related_name='downvotedAnswers', to='forum.Answer')),
                ('groups', models.ManyToManyField(to='groups.Group')),
                ('upvotedAnswers', models.ManyToManyField(related_name='upvotedAnswers', to='forum.Answer')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
