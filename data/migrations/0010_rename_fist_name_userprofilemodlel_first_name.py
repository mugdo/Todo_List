# Generated by Django 4.0.3 on 2022-04-20 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_userprofilemodlel_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofilemodlel',
            old_name='fist_name',
            new_name='first_name',
        ),
    ]