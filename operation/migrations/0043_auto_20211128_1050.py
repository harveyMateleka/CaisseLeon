# Generated by Django 3.0 on 2021-11-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0042_cloture_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloture',
            name='datemvt',
            field=models.DateTimeField(db_column='DateMvt'),
        ),
    ]