# Generated by Django 3.0.3 on 2020-03-12 21:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_privateuncovered_privateuncoveredphotos_stalked'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrivateUncovered',
            new_name='PrivateUncoveredacc',
        ),
        migrations.RenameModel(
            old_name='PrivateUncoveredPhotos',
            new_name='PrivateUncoveredPhoto',
        ),
    ]
