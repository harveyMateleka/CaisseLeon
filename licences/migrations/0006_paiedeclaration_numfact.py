# Generated by Django 3.2.2 on 2022-01-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0005_declaration_montpay'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiedeclaration',
            name='numfact',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
