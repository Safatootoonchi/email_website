# Generated by Django 4.0.3 on 2022-04-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail', '0017_alter_filter_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='archive',
            field=models.CharField(default='N', max_length=10),
        ),
        migrations.AddField(
            model_name='filter',
            name='draft',
            field=models.CharField(default='N', max_length=10),
        ),
        migrations.AlterField(
            model_name='filter',
            name='label',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
