# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    operations = [
        migrations.AddField(
            model_name='article',
            name='readnum',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
