# Generated by Django 3.0 on 2021-10-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0027_auto_20211029_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caisse',
            name='motif',
            field=models.TextField(db_column='Motif'),
        ),
    ]