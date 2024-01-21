# Generated by Django 5.0 on 2024-01-21 12:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
    ]
