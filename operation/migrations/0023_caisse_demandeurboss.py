# Generated by Django 3.0 on 2021-10-28 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0022_auto_20211026_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='caisse',
            name='demandeurboss',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
