# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_test_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='test_content',
        ),
    ]
