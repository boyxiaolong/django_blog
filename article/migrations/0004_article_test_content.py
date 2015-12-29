# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_examplemodel_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='test_content',
            field=ckeditor.fields.RichTextField(null=True, verbose_name=b'text'),
        ),
    ]
