# Generated by Django 4.0.3 on 2022-04-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_remove_userprofilemodlel_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodlel',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
