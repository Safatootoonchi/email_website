# Generated by Django 4.0.3 on 2022-04-04 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail', '0009_alter_background_image_alter_email_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='draft',
            field=models.CharField(default='N', max_length=10),
        ),
    ]