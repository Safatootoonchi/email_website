# Generated by Django 4.0.3 on 2022-04-05 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail', '0011_reply_forward'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='archive',
            field=models.CharField(default='N', max_length=10),
        ),
        migrations.AlterField(
            model_name='forward',
            name='to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='title',
            field=models.CharField(default='why', max_length=100),
        ),
    ]
