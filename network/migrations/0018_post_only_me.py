# Generated by Django 4.0.2 on 2022-03-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_post_only_friends_alter_userprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='only_me',
            field=models.BooleanField(default=False),
        ),
    ]
