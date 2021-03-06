# Generated by Django 3.0 on 2021-09-17 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Droit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('entree', 'Onglet Entrée'), ('sortie', 'Onglet Sortie'), ('rapport', 'Onglet Rapport')),
            },
        ),
        migrations.RemoveField(
            model_name='caisse',
            name='typemvt',
        ),
        migrations.AddField(
            model_name='location',
            name='typemvt',
            field=models.CharField(db_column='TypeMvt', default='', max_length=1),
            preserve_default=False,
        ),
    ]
