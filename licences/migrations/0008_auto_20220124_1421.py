# Generated by Django 3.2.2 on 2022-01-24 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0007_mvt_rapport'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaration',
            name='datfin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='declaration',
            name='mode_paie',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
