# Generated by Django 4.0.6 on 2022-07-23 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'default_permissions': (), 'ordering': ['name', 'start_date', 'end_date', 'organization']},
        ),
    ]