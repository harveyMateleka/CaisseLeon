# Generated by Django 3.0.14 on 2022-06-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0011_auto_20220414_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiedeclaration',
            name='name_ordrepaie',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        
    ]