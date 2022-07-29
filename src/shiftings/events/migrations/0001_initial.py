# Generated by Django 4.0.6 on 2022-07-29 17:25

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import shiftings.utils.fields.date_time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='upload/organizations/', verbose_name='Logo')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-Mail')),
                ('telephone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Telephone Number')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('start_date', shiftings.utils.fields.date_time.DateField(help_text='Earliest date where there are shifts available', verbose_name='Start Date')),
                ('end_date', shiftings.utils.fields.date_time.DateField(help_text='Latest date where there are shifts available', verbose_name='End Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('public', models.BooleanField(default=False, help_text='Allow everyone to participate at this event', verbose_name='Public')),
                ('allowed_organizations', models.ManyToManyField(help_text='Organizations which are allowed to participate', to='organizations.organization', verbose_name='Allowed Organizations')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organizations.organization', verbose_name='Organization')),
            ],
            options={
                'ordering': ['name', 'start_date', 'end_date', 'organization'],
                'default_permissions': (),
            },
        ),
    ]
