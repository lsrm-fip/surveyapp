# Generated by Django 4.2.6 on 2023-11-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilelist',
            name='nim',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
