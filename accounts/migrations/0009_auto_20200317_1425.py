# Generated by Django 3.0.3 on 2020-03-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_photosarchive'),
    ]

    operations = [
        migrations.AddField(
            model_name='photosarchive',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='privateuncoveredacc',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='privateuncoveredphoto',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
