# Generated by Django 3.0 on 2021-11-27 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0039_auto_20211127_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='caisse',
            name='zone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='operation.Zone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='affectation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='userzone', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
