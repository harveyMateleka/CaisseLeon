# Generated by Django 3.0 on 2021-10-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0009_auto_20211007_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='typemvt',
            field=models.CharField(blank=True, db_column='TypeMvt', max_length=1, null=True),
        ),
    ]