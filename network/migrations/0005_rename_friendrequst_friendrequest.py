# Generated by Django 4.0.2 on 2022-03-09 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_userprofile_friends'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FriendRequst',
            new_name='FriendRequest',
        ),
    ]