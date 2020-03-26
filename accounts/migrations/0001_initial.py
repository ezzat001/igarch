# Generated by Django 3.0.3 on 2020-02-24 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('followers', models.IntegerField(blank=True, null=True)),
                ('following', models.IntegerField(blank=True, null=True)),
                ('mutual', models.IntegerField(blank=True, null=True)),
                ('dont_follow_you_back', models.IntegerField(blank=True, null=True)),
                ('you_dont_follow_back', models.IntegerField(blank=True, null=True)),
                ('unfollowed_you', models.IntegerField(blank=True, null=True)),
                ('followers_list', models.TextField(blank=True, null=True)),
                ('following_list', models.TextField(blank=True, null=True)),
                ('mutual_list', models.TextField(blank=True, null=True)),
                ('dont_follow_you_back_list', models.TextField(blank=True, null=True)),
                ('you_dont_follow_back_list', models.TextField(blank=True, null=True)),
                ('unfollowed_you_list', models.TextField(blank=True, null=True)),
                ('private_account', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
