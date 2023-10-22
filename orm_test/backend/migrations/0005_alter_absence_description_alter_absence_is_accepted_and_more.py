# Generated by Django 4.2.1 on 2023-10-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_timecorrection_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='is_accepted',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetitem',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='permissionuser',
            name='is_accepted',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
