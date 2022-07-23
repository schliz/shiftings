# Generated by Django 4.0.6 on 2022-07-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_membership_options_alter_shifter_options'),
        ('organizations', '0002_alter_organization_options_alter_organization_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='helpers',
            field=models.ManyToManyField(blank=True, null=True, related_name='organizations_helper', to='accounts.membership', verbose_name='Helpers'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='managers',
            field=models.ManyToManyField(blank=True, null=True, related_name='managed_organizations', to='accounts.membership', verbose_name='Manager'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='organization_memberships', to='accounts.membership', verbose_name='Members'),
        ),
    ]