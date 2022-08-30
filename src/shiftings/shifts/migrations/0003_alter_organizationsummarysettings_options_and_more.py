# Generated by Django 4.0.6 on 2022-08-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_alter_recurringshift_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationsummarysettings',
            options={'default_permissions': ()},
        ),
        migrations.AlterField(
            model_name='participant',
            name='display_name',
            field=models.CharField(blank=True, help_text='Display Name is optional, and will be shown instead of the username', max_length=100, null=True, verbose_name='Display Name'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='max_users',
            field=models.PositiveIntegerField(default=0, verbose_name='Maximum Users'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='required_users',
            field=models.PositiveIntegerField(default=0, verbose_name='Required Users'),
        ),
    ]