# Generated by Django 5.0.6 on 2024-07-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rhythm', '0005_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='song',
            name='song',
            field=models.FileField(upload_to='images'),
        ),
    ]
