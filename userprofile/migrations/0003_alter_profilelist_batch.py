# Generated by Django 4.2.6 on 2023-11-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profilelist_nim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelist',
            name='batch',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]