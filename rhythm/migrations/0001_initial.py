# Generated by Django 5.0.6 on 2024-05-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('singer', models.CharField(max_length=2000)),
                ('Tags', models.CharField(max_length=2000)),
                ('image', models.ImageField(upload_to='images')),
                ('song', models.FileField(upload_to='images')),
            ],
        ),
    ]
