# Generated by Django 3.0.3 on 2020-03-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_stalkedaction_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stalkedaction',
            name='pic',
            field=models.TextField(),
        ),
    ]
