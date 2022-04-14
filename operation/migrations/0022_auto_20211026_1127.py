# Generated by Django 3.0 on 2021-10-26 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0021_auto_20211022_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='caisse',
            name='lettre',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='etatbesoin',
            name='etat',
            field=models.CharField(choices=[('N', 'Normal'), ('C', 'Caisse'), ('A', 'Admin'), ('V', 'Verificateur')], default='N', max_length=1),
        ),
    ]
