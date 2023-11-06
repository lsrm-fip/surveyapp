# Generated by Django 4.2.6 on 2023-11-06 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_alter_profilelist_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilelist',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='profilelist',
            name='fullname',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profilelist',
            name='nim',
            field=models.CharField(max_length=22, null=True),
        ),
    ]
