# Generated by Django 4.0.9 on 2023-02-09 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_alter_shifttype_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationsummarysettings',
            name='default_shift_types',
        ),
    ]