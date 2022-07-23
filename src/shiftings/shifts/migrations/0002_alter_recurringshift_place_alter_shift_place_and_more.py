# Generated by Django 4.0.6 on 2022-07-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringshift',
            name='place',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Place'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='place',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Place'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='warnings',
            field=models.TextField(blank=True, null=True, verbose_name='Warning'),
        ),
    ]