# Generated by Django 4.0.3 on 2022-04-10 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_group_picture_alter_group_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='picture',
            field=models.ImageField(default='chat.png', null=True, upload_to=''),
        ),
    ]
