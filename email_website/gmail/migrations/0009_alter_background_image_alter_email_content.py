# Generated by Django 4.0.3 on 2022-04-04 20:07

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail', '0008_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='statics/background'),
        ),
        migrations.AlterField(
            model_name='email',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
