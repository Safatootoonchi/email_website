# Generated by Django 4.0.3 on 2022-04-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail', '0004_emailchart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
