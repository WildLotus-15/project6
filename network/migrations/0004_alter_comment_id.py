# Generated by Django 4.0.3 on 2022-04-21 11:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_userprofile_bio_alter_userprofile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
