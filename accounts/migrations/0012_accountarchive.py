# Generated by Django 3.0.3 on 2020-03-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200320_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountArchive',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('join_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
