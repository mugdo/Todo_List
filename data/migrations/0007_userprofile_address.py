# Generated by Django 4.0.3 on 2022-04-20 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
