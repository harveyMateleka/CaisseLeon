# Generated by Django 3.0 on 2021-09-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20210917_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taux',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('taux', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]