# Generated by Django 4.0.2 on 2022-03-10 15:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_friendrequest_network_friendrequest_prevent_self_follow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]